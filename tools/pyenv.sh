# Sourced by the build scripts. `py SCRIPT ARGS` runs a Python tool with the packages the
# build needs: from this Python if it has them, else from nix-shell (NixOS), else it
# says what to install.
PY_PKGS='jinja2 markdown-it-py mdit-py-plugins pypdf playwright'
py() {
  if python3 -c 'import jinja2, markdown_it, mdit_py_plugins, pypdf, playwright' 2>/dev/null; then
    python3 -I "$@"
  elif command -v nix-shell >/dev/null; then
    nix-shell -p "python3.withPackages (ps: with ps; [$PY_PKGS])" --run "python3 -I $(printf '%q ' "$@")"
  else
    echo "Missing Python packages: pip install $PY_PKGS (and python3 -m playwright install chromium)" >&2
    return 1
  fi
}
