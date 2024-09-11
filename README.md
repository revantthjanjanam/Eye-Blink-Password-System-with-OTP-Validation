
```markdown
# Eye Blink Password Detection System

This project is an Eye Blink Password Detection System that uses a webcam to detect eye blinks and allows a user to unlock the system using a predefined blink sequence. The system captures and verifies an eye blink pattern (like 'LRBB' for Left eye closed, Right eye closed, Both eyes closed) and sends an OTP (One-Time Password) via email for final validation before granting access.

## Features

- Real-time detection of left and right eye blinks using Haar Cascade Classifiers.
- Blink sequence detection to match the predefined password.
- Email alert with an OTP and a photo attachment of the person trying to access the system.
- System lock after multiple failed OTP attempts.

## Dependencies

Before running the project, ensure you have installed the following libraries:

- [OpenCV](https://pypi.org/project/opencv-python/) (`cv2`)
- [Numpy](https://pypi.org/project/numpy/) (`numpy`)
- [Imutils](https://pypi.org/project/imutils/) (for easier video stream management)
- [smtplib](https://docs.python.org/3/library/smtplib.html) (for sending emails)
- [SSL](https://docs.python.org/3/library/ssl.html) (for secure email transmission)

You can install the required dependencies by running:

```bash
pip install opencv-python numpy imutils
```

## How It Works

1. **Eye Detection**: 
   - The system uses Haar Cascade Classifiers to detect the left and right eyes in real-time using the webcam feed.
   
2. **Blink Detection**:
   - The states of the eyes (open/closed) are tracked for each frame. Based on these states, the system records the blink sequence: 
     - 'L' for Left eye closed
     - 'R' for Right eye closed
     - 'B' for Both eyes closed
     - 'O' for Both eyes open
   
3. **Blink Sequence Validation**:
   - The user is required to blink in a specific sequence to unlock the system. The default password is `'LRBB'` (Left eye closed -> Right eye closed -> Both eyes closed -> Both eyes closed).
   
4. **Email Alert with OTP**:
   - Once the blink sequence matches the predefined password, the system captures an image and sends it along with a randomly generated OTP to the user's email. The user must enter the OTP to access the system.
   
5. **OTP Verification**:
   - The user has three attempts to enter the correct OTP. If the correct OTP is entered, the system grants access; otherwise, the system remains locked.

## Usage

1. **Run the script**: 
   Start the program by running the Python script:
   ```bash
   python eye_blink_password.py
   ```

2. **Blink in sequence**: 
   Blink your eyes in the predefined sequence (default: `'LRBB'`) in front of the webcam.

3. **Enter OTP**: 
   After a successful blink sequence, an OTP will be sent to your registered email along with the captured image. Enter the OTP to unlock the system.

## Configuration

- **Password**: You can modify the predefined blink password by changing the `password` variable in the code:
   ```python
   password = 'LRBB'  # Example password: Left, Right, Both, Both closed
   ```

- **Email Configuration**: 
   Replace the `user` and `password` variables with your Gmail account credentials. The system uses Gmail's SMTP server to send the OTP email.

   ```python
   user = "your_email@gmail.com"
   password = "your_generated_app_password"
   ```

   Ensure you have set up an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if 2-factor authentication is enabled on your Gmail account.

## Project Structure

- **haarcascades/**: This folder contains the XML files for the Haar Cascade Classifiers used for detecting left and right eyes.
- **eye_blink_password.py**: The main script that runs the eye blink detection system.
- **captured_image.jpg**: The image captured when the blink sequence matches the password.

## Future Enhancements

- Implement a more robust facial recognition system to enhance security.
- Improve the blink detection algorithm for better accuracy.
- Add more user interaction features, such as multi-user support with different blink passwords.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

This README provides a clear overview of the project, how it works, the setup process, and the usage instructions. You can modify it further based on your specific needs or enhancements.
