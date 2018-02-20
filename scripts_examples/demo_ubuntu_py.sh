#!/bin/sh

echo "start demo..."

echo "DEMO FOR CREATE PLATFORM OPERATION"

echo "1. create platform"
python3 surepatch.py --action=create_platform --platform=debtest --description=debtestPlatform

echo "DEMO FOR CREATE PROJECT OPERATION"

echo "2. create project OS auto system none"
python3 surepatch.py --platform=debtest --action=create_project --project=os_none --target=[os] --file=[no]

echo "3. create project OS auto system from_path /home/user/ubuntu_packages.txt"
python3 surepatch.py --platform=debtest --action=create_project --project=os_path --target=[os] --file=[/home/user/ubuntu_packages.txt]

echo "4. create project PIP auto system none"
python3 surepatch.py --platform=debtest --action=create_project --project=pip_none --target=[pip]

echo "5. create project PIP3 auto system none"
python3 surepatch.py --platform=debtest --action=create_project --project=pip3_none --target=[pip3]

echo "6. create project REQ auto system from_path /home/user/requirements.txt"
python3 surepatch.py --platform=debtest --action=create_project --project=req_path --target=req --file=/home/user/requirements.txt

echo "7. create project REQ3 auto system from path /home/user/requirements.txt"
python3 surepatch.py --platform=debtest --action=create_project --project=req3_path --target=req3 --file=/home/user/requirements.txt

echo "8. create project NPM auto system none"
python3 surepatch.py --platform=debtest --action=create_project --project=npm_none --target=npm

echo "9. create project NPM local auto system from path --file=/home/user/workspace/node"
python3 surepatch.py --platform=debtest --action=create_project --project=npm_local_none --target=npm_local --file=/home/user/workspace/node

echo "10. create project NPM auto system from path package.json"
python3 surepatch.py --platform=debtest --action=create_project --project=npm_package_json --target=package_json --file=/home/user/package.json

echo "11. create project NPM auto system path package-lock.json"
python3 surepatch.py --platform=debtest --action=create_project --project=npm_package_lock_json --target=package_lock_json --file=/home/user/package-lock.json

echo "12. create project GEM auto system none"
python3 surepatch.py --platform=debtest --action=create_project --project=gem_none --target=gem

echo "13. create project GEMFILE auto system from path /home/user/Gemfile"
python3 surepatch.py --platform=debtest --action=create_project --project=gemfile --target=gemfile --file=/home/user/Gemfile

echo "14. create project GEMFILE.lock auto system from path /home/user/Gemfile.lock"
python3 surepatch.py --platform=debtest --action=create_project --project=gemfile_lock --target=gemfile_lock --file=/home/user/Gemfile.lock

echo "15. create project PHP Composer JSON auto system from path /home/user/composer1.json"
python3 surepatch.py --platform=debtest --action=create_project --project=php_composer_json --target=php_composer_json --file=/home/user/composer1.json

echo "16. create project PHP Composer Lock auto system from path /home/user/composer1.lock"
python3 surepatch.py --platform=debtest --action=create_project --project=php_composer_lock --target=php_composer_lock --file=/home/user/composer1.lock

echo "17. create project POM auto system from path /home/user/pom.xml"
python3 surepatch.py --platform=debtest --action=create_project --project=pom --target=pom --file=/home/user/pom.xml

echo "18. create project YARN auto system from path /home/user/yarn.lock"
python3 surepatch.py --platform=debtest --action=create_project --project=yarn --target=yarn --file=/home/user/yarn.lock

echo "19. create project USER auto user from path /home/user/user_packages.txt"
python3 surepatch.py --platform=debtest --action=create_project --project=user_path --format=user --file=/home/user/user_packages.txt

echo "20. create project USER manual"
python3 surepatch.py --platform=debtest --action=create_project --project=user_manual --format=user --method=manual


echo "DEMO FOR CREATE SET OPERATIONS"


echo "21. create project for component set tests"
python3 surepatch.py --platform=debtest --action=create_project --project=settest --format=user --file=/home/user/user_packages.txt



echo "22. create set OS auto system none"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=os

echo "23. create set OS auto system from path /home/user/ubuntu_packages.txt"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=os --file=/home/user/ubuntu_packages.txt

echo "24. create project PIP auto system none"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --project=pip_none --target=[pip]

echo "25. create project PIP3 auto system none"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=[pip3]

echo "26. create project REQ auto system from_path /home/user/requirements.txt"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=req --file=/home/user/requirements.txt

echo "27. create project REQ3 auto system from path /home/user/requirements.txt"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=req3 --file=/home/user/requirements.txt

echo "28. create project NPM auto system none"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=npm

echo "29. create project NPM local auto system from path --file=/home/user/workspace/node"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=npm_local --file=/home/user/workspace/node

echo "30. create project NPM auto system from path package.json"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=package_json --file=/home/user/package.json

echo "31. create project NPM auto system path package-lock.json"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=package_lock_json --file=/home/user/package-lock.json

echo "32. create project GEM auto system none"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=gem

echo "33. create project GEMFILE auto system from path /home/user/Gemfile"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=gemfile --file=/home/user/Gemfile

echo "34. create project GEMFILE.lock auto system from path /home/user/Gemfile.lock"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=gemfile_lock --file=/home/user/Gemfile.lock

echo "35. create project PHP Composer JSON auto system from path /home/user/composer1.json"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=php_composer_json --file=/home/user/composer1.json

echo "36. create project PHP Composer Lock auto system from path /home/user/composer1.lock"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=php_composer_lock --file=/home/user/composer1.lock

echo "37. create project POM auto system from path /home/user/pom.xml"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=pom --file=/home/user/pom.xml

echo "38. create project YARN auto system from path /home/user/yarn.lock"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --target=yarn --file=/home/user/yarn.lock

echo "39. create project USER auto user from path /home/user/user_packages.txt"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --format=user --file=/home/user/user_packages.txt

echo "40. create project USER manual"
python3 surepatch.py --platform=debtest --action=create_set --project=settest --format=user --method=manual


echo "DEMO FOR MULTITARGET OPERATIONS"

echo "41. create project for OS, PIP, POM, GEM and Gemfile"
python3 surepatch.py --action=create_project --platform=debtest --project=multitest2 --target=[os,pip,pom,gem,gemfile] --file=[no,no,/home/user/pom.xml,no,/home/user/Gemfile]

echo "42. create set for YARN, PIP3 and Gemfile.lock"
python3 surepatch.py --action=create_set --platform=debtest --project=settest --target=[yarn,pip3,gemfile_lock] --file=[/home/user/yarn.lock,no,/home/user/Gemfile.lock]


echo "DEMO FOR SHOW OPERATIONS"


echo "43. show platforms"
python3 surepatch.py --action=show_platforms

echo "44. show projects"
python3 surepatch.py --action=show_projects --platform=debtest

echo "45. show set"
python3 surepatch.py --action=show_set --platform=debtest --project=settest

echo "46. show issues"
python3 surepatch.py --action=show_issues --platform=debtest --project=settest --file=/home/user/issues_report.txt

echo "complete..."