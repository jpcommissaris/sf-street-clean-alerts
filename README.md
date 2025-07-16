# sf-street-clean-alerts

## What is this?
This is an API that alerts you to the next scheduled street cleaning date, based on the location input. 

## Apple shorcut
Automatically query this API on carplay disconnect via apple shortcut:
TODO

Why carplay disconnect?:
- This is the best way i know of to determine when you've parked your car. As of writing this, apple doesn't expose their "parked car" feature on apple maps to third parties.

Does this api store your location data?:
NO



### Running in Development Mode
To run the app in development mode, use the `main.py` script:

- Python 3.x
- Add venv (recommended): `python3 -m venv venv`
- `source venv/bin/activate`
- Required dependencies (install via `pip`):
  ```bash
  pip install -r requirements.txt
  ```

```bash
python main.py
```
