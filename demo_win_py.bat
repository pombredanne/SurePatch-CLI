echo "start demo..."

echo "DEMO FOR CREATE PLATFORM OPERATION"

echo "1. create platform"
C:\Python36\python.exe surepatch.py --action=create_platform --platform=wintest --description=wintestPlatform

echo "DEMO FOR CREATE PROJECT OPERATION"

echo "2. create project OS auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=os_none --target=[os] --file=[no]

echo "3. create project OS auto system from_path c:\windows_packages.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=os_path --target=[os] --file=[c:\windows_packages.txt]

echo "4. create project PIP auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=pip_none --target=[pip]

echo "5. create project PIP3 auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=pip3_none --target=[pip3]

echo "6. create project REQ auto system from_path c:\requirements.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=req_path --target=req --file=c:\requirements.txt

echo "7. create project REQ3 auto system from path c:\requirements.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=req3_path --target=req3 --file=c:\requirements.txt

echo "8. create project NPM auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=npm_none --target=npm

echo "9. create project NPM local auto system from path --file=c:\workspace/node"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=npm_local_none --target=npm_local --file=c:\workspace/node

echo "10. create project NPM auto system from path package.json"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=npm_package_json --target=package_json --file=c:\package.json

echo "11. create project NPM auto system path package-lock.json"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=npm_package_lock_json --target=package_lock_json --file=c:\package-lock.json

echo "12. create project GEM auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=gem_none --target=gem

echo "13. create project GEMFILE auto system from path c:\Gemfile"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=gemfile --target=gemfile --file=c:\Gemfile

echo "14. create project GEMFILE.lock auto system from path c:\Gemfile.lock"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=gemfile_lock --target=gemfile_lock --file=c:\Gemfile.lock

echo "15. create project PHP Composer JSON auto system from path c:\composer1.json"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=php_composer_json --target=php_composer_json --file=c:\composer1.json

echo "16. create project PHP Composer Lock auto system from path c:\composer1.lock"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=php_composer_lock --target=php_composer_lock --file=c:\composer1.lock

echo "17. create project POM auto system from path c:\pom2.xml"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=pom --target=pom --file=c:\pom2.xml

echo "18. create project YARN auto system from path c:\yarn.lock"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=yarn --target=yarn --file=c:\yarn.lock

echo "19. create project USER auto user from path c:\user_packages.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=user_path --format=user --file=c:\user_packages.txt

echo "20. create project USER manual"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=user_manual --format=user --method=manual


echo "DEMO FOR CREATE SET OPERATIONS"


echo "21. create project for component set tests"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_project --project=settest --format=user --file=c:\user_packages.txt



echo "22. create set OS auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=os

echo "23. create set OS auto system from path c:\windows_packages.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=os --file=c:\windows_packages.txt

echo "24. create project PIP auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --project=pip_none --target=[pip]

echo "25. create project PIP3 auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=[pip3]

echo "26. create project REQ auto system from_path c:\requirements.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=req --file=c:\requirements.txt

echo "27. create project REQ3 auto system from path c:\requirements.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=req3 --file=c:\requirements.txt

echo "28. create project NPM auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=npm

echo "29. create project NPM local auto system from path --file=c:\workspace/node"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=npm_local --file=c:\workspace/node

echo "30. create project NPM auto system from path package.json"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=package_json --file=c:\package.json

echo "31. create project NPM auto system path package-lock.json"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=package_lock_json --file=c:\package-lock.json

echo "32. create project GEM auto system none"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=gem

echo "33. create project GEMFILE auto system from path c:\Gemfile"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=gemfile --file=c:\Gemfile

echo "34. create project GEMFILE.lock auto system from path c:\Gemfile.lock"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=gemfile_lock --file=c:\Gemfile.lock

echo "35. create project PHP Composer JSON auto system from path c:\composer1.json"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=php_composer_json --file=c:\composer1.json

echo "36. create project PHP Composer Lock auto system from path c:\composer1.lock"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=php_composer_lock --file=c:\composer1.lock

echo "37. create project POM auto system from path c:\pom2.xml"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=pom --file=c:\pom2.xml

echo "38. create project YARN auto system from path c:\yarn.lock"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --target=yarn --file=c:\yarn.lock

echo "39. create project USER auto user from path c:\user_packages.txt"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --format=user --file=c:\user_packages.txt

echo "40. create project USER manual"
C:\Python36\python.exe surepatch.py --platform=wintest --action=create_set --project=settest --format=user --method=manual


echo "DEMO FOR MULTITARGET OPERATIONS"

echo "41. create project for OS, PIP, POM, GEM and Gemfile"
C:\Python36\python.exe surepatch.py --action=create_project --platform=wintest --project=multitest2 --target=[os,pip,pom,gem,gemfile] --file=[no,no,c:\pom2.xml,no,c:\Gemfile]

echo "42. create set for YARN, PIP3 and Gemfile.lock"
C:\Python36\python.exe surepatch.py --action=create_set --platform=wintest --project=settest --target=[yarn,pip3,gemfile_lock] --file=[c:\yarn.lock,no,c:\Gemfile.lock]


echo "DEMO FOR SHOW OPERATIONS"


echo "43. show platforms"
C:\Python36\python.exe surepatch.py --action=show_platforms

echo "44. show projects"
C:\Python36\python.exe surepatch.py --action=show_projects --platform=wintest

echo "45. show set"
C:\Python36\python.exe surepatch.py --action=show_set --platform=wintest --project=settest

echo "46. show issues"
C:\Python36\python.exe surepatch.py --action=show_issues --platform=wintest --project=settest --file=c:\issues_report.txt

echo "complete..."