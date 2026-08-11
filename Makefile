# README.org is the source; README.md is generated from it.
#
# README.org is what you edit.  It also tangles diet_problem.py, which the
# Markdown export cannot do.  README.md exists because pyproject.toml names it
# as the packaging readme and PyPI wants Markdown, and because GitHub renders
# README.md in preference to README.org.
#
# Do not edit README.md by hand: `make readme` will overwrite it.

EMACS ?= emacs

# Kept on one line deliberately: a backslash-continuation inside the quoted
# --eval is passed through to Emacs literally and breaks the form.
EXPORT_MD = (progn (require (quote org)) (require (quote ox-md)) (setq make-backup-files nil org-export-with-toc nil) (find-file "$(1)") (org-md-export-to-markdown))

.PHONY: all readme readme-check

all: readme

readme: README.md

README.md: README.org
	$(EMACS) -Q --batch --eval '$(call EXPORT_MD,README.org)'

# Fail if README.md is out of date with respect to README.org, without
# modifying the working tree.  Useful in CI, or before tagging a release.
# The export runs from inside the temp directory so the filename in the elisp
# stays the literal "README.org".  Interpolating a shell variable into the
# --eval would require double quotes outside, which collide with the double
# quotes the elisp itself needs.
readme-check:
	@here=$$(pwd); tmp=$$(mktemp -d); \
	cp README.org $$tmp/README.org; \
	( cd $$tmp && $(EMACS) -Q --batch --eval '$(call EXPORT_MD,README.org)' >/dev/null 2>&1 ); \
	if diff -q $$here/README.md $$tmp/README.md >/dev/null 2>&1; then \
	  echo "README.md is up to date."; rm -rf $$tmp; \
	else \
	  echo "README.md is STALE; run 'make readme'."; \
	  diff -u $$here/README.md $$tmp/README.md | head -40; rm -rf $$tmp; exit 1; \
	fi
