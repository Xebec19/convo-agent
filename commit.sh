echo "Enter commit message"
read msg

ruff check api/ --fix

git add .
git commit -m "$msg"
git push