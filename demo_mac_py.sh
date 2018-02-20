#!/bin/sh

echo "start demo..."

echo "DEMO FOR CREATE PLATFORM OPERATION"

echo "1. create platform"
python3 surepatch.py --action=create_platform --platform=mactest --description=mactestPlatform

echo "DEMO FOR CREATE PROJECT OPERATION"

echo "2. create project OS auto system none"
python3 surepatch.py --platform=mactest --action=create_project --project=os_none --target=[os] --file=[no]

echo "3. create project OS auto system from_path /Users/admin/packages_examples/packages_examples/mac_rep.txt"
python3 surepatch.py --platform=mactest --action=create_project --project=os_path --target=[os] --file=[/Users/admin/packages_examples/mac_rep.txt]

echo "4. create project PIP auto system none"
python3 surepatch.py --platform=mactest --action=create_project --project=pip_none --target=[pip]

echo "5. create project PIP3 auto system none"
python3 surepatch.py --platform=mactest --action=create_project --project=pip3_none --target=[pip3]

echo "6. create project REQ auto system from_path /Users/admin/packages_examples/requirements.txt"
python3 surepatch.py --platform=mactest --action=create_project --project=req_path --target=req --file=/Users/admin/packages_examples/requirements.txt

echo "7. create project REQ3 auto system from path /Users/admin/packages_examples/requirements.txt"
python3 surepatch.py --platform=mactest --action=create_project --project=req3_path --target=req3 --file=/Users/admin/packages_examples/requirements.txt

echo "8. create project NPM auto system none"
python3 surepatch.py --platform=mactest --action=create_project --project=npm_none --target=npm

echo "9. create project NPM local auto system from path --file=/Users/admin/packages_examples/"
python3 surepatch.py --platform=mactest --action=create_project --project=npm_local_none --target=npm_local --file=/Users/admin/packages_examples/

echo "10. create project NPM auto system from path package.json"
python3 surepatch.py --platform=mactest --action=create_project --project=npm_package_json --target=package_json --file=/Users/admin/packages_examples/package.json

echo "11. create project NPM auto system path package-lock.json"
python3 surepatch.py --platform=mactest --action=create_project --project=npm_package_lock_json --target=package_lock_json --file=/Users/admin/packages_examples/package-lock.json

echo "12. create project GEM auto system none"
python3 surepatch.py --platform=mactest --action=create_project --project=gem_none --target=gem

echo "13. create project GEMFILE auto system from path /Users/admin/packages_examples/Gemfile"
python3 surepatch.py --platform=mactest --action=create_project --project=gemfile --target=gemfile --file=/Users/admin/packages_examples/Gemfile

echo "14. create project GEMFILE.lock auto system from path /Users/admin/packages_examples/Gemfile.lock"
python3 surepatch.py --platform=mactest --action=create_project --project=gemfile_lock --target=gemfile_lock --file=/Users/admin/packages_examples/Gemfile.lock

echo "15. create project PHP Composer JSON auto system from path /Users/admin/packages_examples/composer1.json"
python3 surepatch.py --platform=mactest --action=create_project --project=php_composer_json --target=php_composer_json --file=/Users/admin/packages_examples/composer1.json

echo "16. create project PHP Composer Lock auto system from path /Users/admin/packages_examples/composer1.lock"
python3 surepatch.py --platform=mactest --action=create_project --project=php_composer_lock --target=php_composer_lock --file=/Users/admin/packages_examples/composer1.lock

echo "17. create project POM auto system from path /Users/admin/packages_examples/pom2.xml"
python3 surepatch.py --platform=mactest --action=create_project --project=pom --target=pom --file=/Users/admin/packages_examples/pom2.xml

echo "18. create project YARN auto system from path /Users/admin/packages_examples/yarn.lock"
python3 surepatch.py --platform=mactest --action=create_project --project=yarn --target=yarn --file=/Users/admin/packages_examples/yarn.lock

echo "19. create project USER auto user from path /Users/admin/packages_examples/user_packages.txt"
python3 surepatch.py --platform=mactest --action=create_project --project=user_path --format=user --file=/Users/admin/packages_examples/user_packages.txt

echo "20. create project USER manual"
python3 surepatch.py --platform=mactest --action=create_project --project=user_manual --format=user --method=manual


echo "DEMO FOR CREATE SET OPERATIONS"


echo "21. create project for component set tests"
python3 surepatch.py --platform=mactest --action=create_project --project=settest --format=user --file=/Users/admin/packages_examples/user_packages.txt



echo "22. create set OS auto system none"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=os

echo "23. create set OS auto system from path /Users/admin/packages_examples/mac_rep.txt"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=os --file=/Users/admin/packages_examples/mac_rep.txt

echo "24. create project PIP auto system none"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --project=pip_none --target=[pip]

echo "25. create project PIP3 auto system none"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=[pip3]

echo "26. create project REQ auto system from_path /Users/admin/packages_examples/requirements.txt"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=req --file=/Users/admin/packages_examples/requirements.txt

echo "27. create project REQ3 auto system from path /Users/admin/packages_examples/requirements.txt"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=req3 --file=/Users/admin/packages_examples/requirements.txt

echo "28. create project NPM auto system none"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=npm

echo "29. create project NPM local auto system from path --file=/Users/admin/packages_examples/"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=npm_local --file=/Users/admin/packages_examples/

echo "30. create project NPM auto system from path package.json"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=package_json --file=/Users/admin/packages_examples/package.json

echo "31. create project NPM auto system path package-lock.json"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=package_lock_json --file=/Users/admin/packages_examples/package-lock.json

echo "32. create project GEM auto system none"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=gem

echo "33. create project GEMFILE auto system from path /Users/admin/packages_examples/Gemfile"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=gemfile --file=/Users/admin/packages_examples/Gemfile

echo "34. create project GEMFILE.lock auto system from path /Users/admin/packages_examples/Gemfile.lock"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=gemfile_lock --file=/Users/admin/packages_examples/Gemfile.lock

echo "35. create project PHP Composer JSON auto system from path /Users/admin/packages_examples/composer1.json"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=php_composer_json --file=/Users/admin/packages_examples/composer1.json

echo "36. create project PHP Composer Lock auto system from path /Users/admin/packages_examples/composer1.lock"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=php_composer_lock --file=/Users/admin/packages_examples/composer1.lock

echo "37. create project POM auto system from path /Users/admin/packages_examples/pom2.xml"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=pom --file=/Users/admin/packages_examples/pom2.xml

echo "38. create project YARN auto system from path /Users/admin/packages_examples/yarn.lock"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --target=yarn --file=/Users/admin/packages_examples/yarn.lock

echo "39. create project USER auto user from path /Users/admin/packages_examples/user_packages.txt"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --format=user --file=/Users/admin/packages_examples/user_packages.txt

echo "40. create project USER manual"
python3 surepatch.py --platform=mactest --action=create_set --project=settest --format=user --method=manual


echo "DEMO FOR MULTITARGET OPERATIONS"

echo "41. create project for OS, PIP, POM, GEM and Gemfile"
python3 surepatch.py --action=create_project --platform=mactest --project=multitest2 --target=[os,pip,pom,gem,gemfile] --file=[no,no,/Users/admin/packages_examples/pom2.xml,no,/Users/admin/packages_examples/Gemfile]

echo "42. create set for YARN, PIP3 and Gemfile.lock"
python3 surepatch.py --action=create_set --platform=mactest --project=settest --target=[yarn,pip3,gemfile_lock] --file=[/Users/admin/packages_examples/yarn.lock,no,/Users/admin/packages_examples/Gemfile.lock]


echo "DEMO FOR SHOW OPERATIONS"


echo "43. show platforms"
python3 surepatch.py --action=show_platforms

echo "44. show projects"
python3 surepatch.py --action=show_projects --platform=mactest

echo "45. show set"
python3 surepatch.py --action=show_set --platform=mactest --project=settest

echo "46. show issues"
python3 surepatch.py --action=show_issues --platform=mactest --project=settest --file=/Users/admin/packages_examples/issues_report.txt

echo "complete..."