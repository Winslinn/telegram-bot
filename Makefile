all:
	xgettext -d messages -o locales/messages.pot *.py --from-code=UTF-8 -k_
	for po in locales/*/LC_MESSAGES/*.po; do \
		echo "Fixing duplicates in $$po"; \
		msguniq "$$po" -o "$$po.fixed"; \
		mv "$$po.fixed" "$$po"; \
		echo "Updating $$po"; \
		msgmerge --backup=off -U "$$po" locales/messages.pot; \
		echo "Compiling $$po"; \
		msgfmt "$$po" -o "$${po%.po}.mo"; \
	done

clean:
	find locales -name "*.mo" -delete