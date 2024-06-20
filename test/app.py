import os

import taggerview
import argparse

taggerview.app.ApplicationCLI.run(argparse.Namespace(**{
    "configuration": "./debug.configuration.json",
    "noter_file": ".noter.json"
}))

