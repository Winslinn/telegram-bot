extract:
	xgettext -d messages -o locales/messages.pot *.py --from-code=UTF-8 -k_

update: extract
	for po in locales/*/LC_MESSAGES/*.po; do \
		echo "Updating $$po"; \
		msgmerge --backup=off -U "$$po" locales/messages.pot; \
	done

compile:
	for po in locales/*/LC_MESSAGES/*.po; do \
		echo "Compiling $$po"; \
		msgfmt "$$po" -o "$${po%.po}.mo"; \
	done

all: update compile

clean:
	find locales -name "*.mo" -delete

new-lang:
	@if ! locale -a | grep -q "^$(lang)"; then \
		echo "Language $(lang) is not installed in the system"; \
		echo "Installing language $(lang)..."; \
		sudo locale-gen $(lang); \
		sudo update-locale; \
	else \
		echo "Language $(lang) is already installed"; \
	fi
	mkdir -p locales/$(lang)/LC_MESSAGES
	msginit -i locales/messages.pot -o locales/$(lang)/LC_MESSAGES/messages.po -l $(lang)
	msgfmt locales/$(lang)/LC_MESSAGES/messages.po -o locales/$(lang)/LC_MESSAGES/messages.mo
	echo "Language $(lang) added to project!"