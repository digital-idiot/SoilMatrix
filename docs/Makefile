# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = SoilMatrix
SOURCEDIR     = source
BUILDDIR      = build

# Internal variables.
PAPER         =

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH.)
endif

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for convenience
livehtml:
	sphinx-autobuild -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O) --host 0.0.0.0 --port 8000

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(SOURCEDIR)/_autosummary
	rm -rf $(SOURCEDIR)/generated

html-noplot:
	$(SPHINXBUILD) -D plot_gallery=0 -b html $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)/html"
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Use pixi for installation instead of pip
install:
	pixi install

# Additional pixi-based targets
pixi-docs:
	pixi run -e docs docs-build

pixi-docs-live:
	pixi run -e docs docs-live

pixi-docs-clean:
	pixi run -e docs docs-clean

.PHONY: help clean livehtml html-noplot install pixi-docs pixi-docs-live pixi-docs-clean