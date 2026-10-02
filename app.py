#!/usr/bin/env python3
import sys

if len(sys.argv) > 1 and sys.argv[1] in ("server", "--server"):
    from server import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
else:
    from interfaces.cli import main
    main()
