# CI

### Other docs:
* [Migrations](Migrations.md)
* [Seeders](Seeders.md)
* [Readme](../README.md)

**Build types:**
* Server (server) 
* Client (client)
* Ui (client_ui)

### Build for current platform
```shell
./ci generate
  [-t|--output-type     OUTPUT_TYPE     ]
  [-o|--output-dir      OUTPUT_DIR      ]
  [-p|--cross-platform  CROSS_PLATFORM  ] 
  [-m|--cross-machine   CROSS_MACHINE   ]
  [--test               TEST            ]
```

For windows use python:

```shell
.\.venv\Scripts\python.exe ci
```


**Parameters**:
* `OUTPUT_TYPE` - Build type. For default using **ALL TYPES** for current platform.
* `OUTPUT_DIR` - Build directory. Directory will include builds. Default - `build` in root project.
* `CROSS_PLATFORM` - Force set platform name. **!!!Unspecified errors may occur**.
* `CROSS_MACHINE` - Force set architecture name. **!!!Unspecified errors may occur**.
* `TEST` - Flag for enable test mode. Includes all build types for all platforms.
Platform specific scripts disabled.

### Show builder info
Windows:

```shell
.\.venv\Scripts\python.exe ci info [--current-platform CURENT_PLATFORM]
```

For macOS or Linux:

```shell
./ci info [--current-platform CURENT_PLATFORM]
```

**Parameters**
* `CURENT_PLATFORM` - Show only current platform info.