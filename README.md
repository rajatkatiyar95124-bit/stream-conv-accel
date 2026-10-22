# Streaming Convolution Accelerator

\## Design Decisions



\### Architecture

\- \*\*Operation:\*\* 3×3 valid convolution on an 8-bit pixel stream.

\- \*\*Line buffers:\*\* Two line buffers retain the previous two image rows, enabling a 3×3 sliding window without storing the entire image.

\- \*\*Window registers:\*\* Nine pixel registers hold the current 3×3 window.

\- \*\*Arithmetic:\*\* Nine signed 8-bit weights multiply the unsigned 8-bit pixels. The products are accumulated using a pipelined adder tree.

\- \*\*Post-processing:\*\* Add a signed bias, apply ReLU, and saturate the result to the unsigned 8-bit range \[0, 255].

\- \*\*Control:\*\* Row and column counters track pixel positions. Window validity is asserted only when a complete 3×3 window is available.

\- \*\*Streaming interface:\*\* `valid\_in` indicates valid input pixels. `valid\_out` is delayed to align with the arithmetic pipeline.



\### Verification Strategy

\- A Python golden model provides the reference output for convolution, bias, ReLU, and saturation.

\- SystemVerilog RTL will be verified through simulation and compared against the Python reference model.

\- A standalone counter testbench has been simulated successfully in Vivado to validate the basic simulation workflow.



\### Initial Test Configuration

\- Input image: 8×8 unsigned 8-bit pixels.

\- Kernel: Sobel-X, represented using signed 8-bit coefficients.

\- Padding: None (valid convolution).

\- Expected output dimensions: 6×6.

\- Initial bias: 0.

\- Initial right shift: 0.

