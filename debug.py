state = {
  "session":{
    "location2": {
      "lat": 55.753215,
      "lon": 37.622504,
      "accuracy": 15000.0
    },
  }
}

a = state["session"].get('location', {})

print(a)