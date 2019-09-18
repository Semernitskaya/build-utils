import glob

import os
import argparse


def filters_parser(filters_line: str):
    return None if filters_line is None or filters_line.strip().__len__() == 0 else filters_line.split(",")


parser = argparse.ArgumentParser(description='Deploy artifacts from local repository to remote')
parser.add_argument('--url', required=True, help='remote repository URL')
parser.add_argument('--login', required=True, help='login for remote repository')
parser.add_argument('--pwd', required=True, help='password for remote repository')
parser.add_argument('--dir', required=True, help='local repository path')
parser.add_argument('--releases', default='ext-releases-local', help='releases repository name')
parser.add_argument('--snapshots', default='ext-snapshots-local', help='snapshots repository name')
parser.add_argument('--filters', type=filters_parser, help='list of comma-separated filters')
parser.add_argument('--dry_run',
                    type=lambda s: s.lower() == str(True).lower(),
                    default=True,
                    help='defines whether to execute generated commands or not')

args = parser.parse_args()

local_repository_dir = args.dir
extensions = ["jar", "pom"]

if args.dry_run:
    print("Dry run")
print("Filters: {}".format(args.filters))

for extension in extensions:
    for local_filename in glob.iglob(local_repository_dir + '**/*.' + extension, recursive=True):
        if args.filters is None or any(x in local_filename for x in args.filters):
            repository_filename = local_filename.replace(local_repository_dir, "")
            repository_name = args.snapshots if 'SNAPSHOT' in local_filename else args.releases
            cmd = 'curl -u {login}:{password} -X PUT "{repository_url}{repository_name}/{repository_filename}" -T {local_filename}'.format(
                login=args.login,
                password=args.pwd,
                repository_url=args.url,
                repository_name=repository_name,
                repository_filename=repository_filename,
                local_filename=local_filename)
            print(cmd)
            if not args.dry_run:
                os.system(cmd)
