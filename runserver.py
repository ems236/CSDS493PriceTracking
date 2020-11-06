#!/usr/bin/env python3
from server.webapp import app

if __name__ == "__main__":
    app.config["IS_TEST"] = False
    app.run(host='0.0.0.0')
