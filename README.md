# sf-street-clean-alerts

## What is this?
This is an API that alerts you to the next scheduled street cleaning date, based on the location input. 

## Inspiration
Parking my car overnight & waking up the following morning to a $105 ticket 🤦‍♂️ 

## Apple shortcut
Automatically query this API on CarPlay disconnect via Apple Shortcut:
TODO (working on it)

Why use CarPlay Disconnect? (for the shortcut):
- This is the best way I know of to determine when you've parked your car. As of writing this, Apple doesn't expose its "parked car" feature on Apple Maps to third parties.

## Raw API:
TODO (working on exposing it in Docker - completed in dev mode)



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
