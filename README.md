# PyPalette

PyPalette is a simple Python-based color palette generator that displays random colors and allows users to copy hex codes with a click. It was inspired by [coolors.co](https://coolors.co) and was originally created as a side project a couple of years ago.

![PyPalette Screenshot](assets/screenshots/pypalette-showcase.gif)

## Features

- Generates random color palettes.
- Click on a color to copy its hex code to the clipboard.
- Press `Space` to generate a new palette.
- Fetches color names from [The Color API](https://www.thecolorapi.com).



## Installation

### Prerequisites

- Python 3.8+
- `pip` installed

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/moealkurdi/pypalette.git
   cd pypalette
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python main.py
   ```

## Usage

- Click on a color to copy its hex code to the clipboard.
- Press `Space` to generate a new random palette.
- Close the window to exit the program.

## Dependencies

- `pygame` - for UI and event handling
- `pyperclip` - for clipboard functionality
- `requests` - for fetching color names from the API

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
