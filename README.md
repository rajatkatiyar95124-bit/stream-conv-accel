# Streaming Convolution Accelerator

**A streaming 3×3 image convolution accelerator built with SystemVerilog.**

Pixels arrive one per clock cycle, two image rows are buffered, and a pipelined datapath computes convolution outputs. A Python fixed-point golden model serves as the reference for RTL verification.

---

## Project Status

**Current Phase: 2 of 6 — Line Buffer & Sliding Window**

| Phase | Milestone | Status |
|:---:|---|:---:|
| 1 | Setup, golden model, architecture & timing sketches | ✅ Complete |
| 2 | Line buffer & 3×3 window generator | 🔄 In Progress |
| 3 | MAC array, adder tree, bias, ReLU & saturation | ⏳ Planned |
| 4 | Top-level integration & self-checking testbench | ⏳ Planned |
| 5 | Synthesis, pipeline-depth & memory experiments | ⏳ Planned |
| 6 | Image demo & final documentation | ⏳ Planned |

---

## Architecture

The accelerator processes image pixels in raster order and generates a valid 3×3 window without storing the entire image.

![Block diagram](docs/block_diagram.png)

```text
                  ┌─────────────────┐
Pixel Stream ────►│   Line Buffers  │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │  3×3 Window     │
                  │   Generator     │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │  9 Multipliers  │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Pipelined Adder │
                  │      Tree       │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Bias + ReLU +   │
                  │   Saturation    │
                  └────────┬────────┘
                           ▼
                      Output Stream
```

A control unit tracks the row and column counters and generates `valid_out`, aligned with the datapath's pipeline latency.

## Design Specifications

| Parameter | Specification |
|---|---|
| Input pixel | 8-bit unsigned |
| Kernel weight | 8-bit signed |
| Kernel size | 3×3 |
| Multiplication | 9 parallel multipliers |
| Padding | None — valid convolution |
| Input throughput | One pixel per clock when `valid_in` is high |
| Reset | Synchronous, active-high |
| Output activation | ReLU |
| Output format | 8-bit unsigned, saturated |
| Flow control | No backpressure |

### Convolution Behavior

For an input image of height \(H\) and width \(W\), valid convolution produces an output of size:

\[
(H-2)\times(W-2)
\]

The first valid window completes at pixel index:

```text
2*W + 2
```

using zero-based indexing and row-major pixel arrival.

A window is valid when:

```systemverilog
row >= 2 && col >= 2
```

Invalid windows are not repaired or reset. The window registers continue shifting, while `valid_out` remains low for invalid positions.

### Arithmetic Datapath

Each 3×3 window is multiplied element-wise by the kernel weights. The products are accumulated, bias is added, and the result passes through an arithmetic right shift, ReLU, and 8-bit saturation.

The accumulator width is targeted at 20 bits, subject to confirming the supported bias range and overflow behavior.

---

## Timing Analysis

The timing sketch illustrates pixel arrival, valid-window positions, line-buffer contents, and row-boundary behavior.

![Timing sketch](docs/timing_sketch.png)

Key observations:

- Two line buffers retain the previous two image rows.
- Horizontal window registers retain the previous two columns.
- The first valid 3×3 window appears at pixel index `2*W + 2`.
- The number of valid output pixels is `(H - 2) × (W - 2)`.

---

## Repository Structure

```text
stream-conv-accel/
├── rtl/       # Synthesizable SystemVerilog modules
├── tb/        # Testbenches and verification
├── model/     # Python golden model
├── data/      # Test images and expected outputs
├── docs/      # Architecture diagrams and timing sketches
├── scripts/   # Helper and automation scripts
└── README.md  # Project documentation
```

## Python Golden Model

The reference implementation is available at [`model/golden.py`](model/golden.py).

It performs:

1. Valid 3×3 window extraction.
2. Signed-weight multiplication and accumulation.
3. Bias addition and arithmetic right shift.
4. ReLU activation.
5. Saturation to an unsigned 8-bit output.

Run the model with Python and NumPy installed:

```bash
python model/golden.py
```

The golden model will serve as the functional reference for the convolution RTL testbench.

---

## Simulation & Verification

RTL simulation is performed using **AMD Xilinx Vivado (xsim)**.

The repository currently includes an initial counter module and testbench used to validate the simulation workflow. The convolution-specific RTL and self-checking testbench are planned for subsequent phases.

---

## Synthesis & Performance Evaluation

Planned measurements for Phase 5 include:

- Maximum operating frequency (**Fmax**)
- LUT, flip-flop, DSP and BRAM utilization
- Pipeline-depth trade-offs
- Line-buffer versus frame-buffer memory requirements

Results will be documented after synthesis and implementation experiments.

---

## Limitations & Future Work

**Current scope**

- Single-channel image processing
- Fixed 3×3 convolution
- No padding
- No backpressure or ready/valid handshake

**Potential extensions**

- BRAM-based line buffers
- Configurable kernel dimensions
- 2×2 max pooling
- Ready/valid flow control
- Hardware-versus-golden-model regression testing

---

## Tools & Technologies

`SystemVerilog` · `Vivado` · `Python` · `NumPy` · `Git` · `GitHub`

---

*Developed as an RTL design project exploring streaming image processing, hardware pipelining, and verification.*