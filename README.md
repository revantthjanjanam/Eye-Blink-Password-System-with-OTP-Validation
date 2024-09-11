# Eye Blink Password Detection System

The **Eye Blink Password Detection System** allows users to unlock the system by blinking their eyes in a predefined sequence. It uses a webcam to detect eye blinks and verifies the pattern (e.g., `'LRBB'` for Left eye closed, Right eye closed, Both eyes closed twice) before sending an OTP (One-Time Password) to the user's email for final validation.

## Features

- Real-time detection of left and right eye blinks using Haar Cascade Classifiers.
- Blink sequence detection to match a predefined password.
- Sends an OTP via email, with a captured photo of the person attempting to unlock the system.
- Locks the system after multiple failed OTP attempts.

## Dependencies

Ensure you have the following libraries installed before running the project:

- [OpenCV](https://pypi.org/project/opencv-python/) (`cv2`)
- [Numpy](https://pypi.org/project/numpy/) (`numpy`)
- [Imutils](https://pypi.org/project/imutils/) (for easier video stream management)
- [smtplib](https://docs.python.org/3/library/smtplib.html) (for sending emails)
- [SSL](https://docs.python.org/3/library/ssl.html) (for secure email transmission)

Install the required dependencies by running:

```bash
pip install opencv-python numpy imutils
```

## How It Works

1. **Eye Detection**  
   The system uses Haar Cascade Classifiers to detect the left and right eyes in real-time from the webcam feed.

2. **Blink Detection**  
   Eye states (open/closed) are tracked for each frame. Based on these states, the system records the blink sequence:  
   - `'L'` for Left eye closed  
   - `'R'` for Right eye closed  
   - `'B'` for Both eyes closed  
   - `'O'` for Both eyes open  

3. **Blink Sequence Validation**  
   The user must blink in a specific sequence to unlock the system. The default password is `'LRBB'` (Left eye closed -> Right eye closed -> Both eyes closed -> Both eyes closed).

4. **Email Alert with OTP**  
   Once the blink sequence matches the predefined password, the system captures an image and sends it along with a randomly generated OTP to the user’s email. The user must enter the OTP to gain access.

5. **OTP Verification**  
   The user has three attempts to enter the correct OTP. If the OTP is correct, the system grants access. If not, the system remains locked after multiple failed attempts.

## Usage

1. **Run the Script**  
   Start the program by running the following command:

   ```bash
   python eye_blink_password.py
   ```

2. **Blink in Sequence**  
   Blink your eyes in the predefined sequence (default: `'LRBB'`) in front of the webcam.

3. **Enter OTP**  
   After a successful blink sequence, an OTP will be sent to your registered email along with the captured image. Enter the OTP to unlock the system.

## Configuration

- **Blink Password**  
   You can modify the predefined blink password by changing the `password` variable in the code:

   ```python
   password = 'LRBB'  # Example password: Left, Right, Both, Both closed
   ```

- **Email Configuration**  
   Replace the `user` and `password` variables with your Gmail credentials. The system uses Gmail's SMTP server to send the OTP.

   ```python
   user = "your_email@gmail.com"
   password = "your_generated_app_password"
   ```

   Make sure to set up an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if you have 2-factor authentication enabled on your Gmail account.

## Project Structure

- **haarcascades/**: Folder containing XML files for Haar Cascade Classifiers (for detecting eyes).
- **eye_blink_password.py**: The main Python script that runs the eye blink detection system.
- **captured_image.jpg**: The image captured when the blink sequence matches the password.

## Future Enhancements

- Integrate a facial recognition system for additional security.
- Improve the blink detection algorithm to increase accuracy.
- Add multi-user support with customizable blink passwords.
