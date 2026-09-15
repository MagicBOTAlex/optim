{
  description = "Python development environment with UV (FHS)";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        # Explicit python environment containing standard system extensions
        myPython = pkgs.python312.withPackages (
          ps: with ps; [
            tkinter
            setuptools
            pyqt6
            pyside6
          ]
        );
      in
      {
        devShells.default =
          (pkgs.buildFHSEnv {
            name = "python-uv-dev";
            targetPkgs =
              pkgs: with pkgs; [
                glibc
                stdenv.cc.cc.lib

                # Core environment
                myPython
                uv

                # Window system components
                gcc
                pkg-config
                zlib
                libffi
                openssl
                ncurses
                readline
                sqlite
                tk
                xz
                libX11
                libxcb
                xcbutilwm
                xcbutilimage
                xcbutilkeysyms
                xcbutilrenderutil
                libXcursor
                libXcomposite
                libXdamage
                libXext
                libXfixes
                libXi
                libXrender
                libXtst
                libXrandr
                libXinerama
                libxkbcommon
                dbus
                xcbutilcursor
                fontconfig

                # Utilities
                git
                curl
                wget
                which

                # Math & rendering headers
                libxml2
                libxslt
                libjpeg
                libpng
                freetype
                blas
                lapack
                gfortran
                portaudio
                libGL
                libGLU
                glib
              ];

            runScript = "bash";

            profile = ''
              # Block UV from managing custom internet python runtimes
              export UV_PYTHON="/usr/bin/python3"
              export UV_PYTHON_DOWNLOADS="never"
              export UV_SYSTEM_PYTHON=1

              # Graphics system requirements
              export LD_LIBRARY_PATH="/usr/lib:/usr/lib64:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
              unset QT_QPA_PLATFORMTHEME
              unset QT_STYLE_OVERRIDE
              unset KDE_FULL_SESSION
              unset KDE_SESSION_VERSION

              export QT_PLUGIN_PATH="${pkgs.qt6.qtbase}/${pkgs.qt6.qtbase.qtPluginPrefix}"
              export QT_QPA_PLATFORM=xcb
              export MPLBACKEND="TkAgg"

              # CRITICAL FIX: Locate the real compiled nix extension folder and inject it directly into Python's path
              NIX_TKINTER_PATH="${pkgs.python312Packages.tkinter}/lib/python3.12/site-packages"
              NIX_QT_PATH="${pkgs.python312Packages.pyqt6}/lib/python3.12/site-packages"
              export PYTHONPATH="$NIX_TKINTER_PATH:$NIX_QT_PATH:$PYTHONPATH"

              # Setup defaults if initializing cold
              if [ ! -f "pyproject.toml" ]; then
                  uv init --python python3.12
                  uv add jupyter ipykernel ipywidgets notebook torch 
                  uv add --dev black ruff isort pytest
              fi

              KERNEL="$(basename "$PWD")"
              jupyter kernelspec list 2>/dev/null | grep -qw "$KERNEL" || \
                uv run python -m ipykernel install --user --name="$KERNEL" --display-name="Python ($KERNEL)"

              # Sync project requirements directly to the system environment
              uv sync --system

              echo "Environment ready!"
              python3 -c "import _tkinter; import tkinter; print('Tkinter loaded successfully!')"
              python3 --version

              source ./.venv/bin/activate
            '';
          }).env;
      }
    );
}
