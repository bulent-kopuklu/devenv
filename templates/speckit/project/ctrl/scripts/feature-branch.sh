#!/usr/bin/env bash
# impl'in reposunda yeni özelliğin branch'ini güncel main'den açar. Branch adını
# spec-kit'in create-new-feature.sh'i verir (ör. 002-backup).
#   scripts/feature-branch.sh <name>

set -euo pipefail
name="${1:?usage: scripts/feature-branch.sh <name>}"
impl="{{ROOT}}/{{NAME}}-impl"

if [ -n "$(git -C "$impl" status --porcelain)" ]; then
  echo "impl'de commit'lenmemiş değişiklik var; branch açılmadı" >&2
  git -C "$impl" status --short >&2
  exit 1
fi
if [ -n "$(git -C "$impl" log --branches --not --remotes --oneline)" ]; then
  echo "impl'de push'lanmamış commit var; branch açılmadı" >&2
  git -C "$impl" log --branches --not --remotes --oneline >&2
  exit 1
fi

git -C "$impl" switch main
git -C "$impl" pull --ff-only

# Numara main'deki specs/'e göre hesaplanır; bu yüzden main'e geçtikten sonra.
branch=$("$impl/.specify/scripts/bash/create-new-feature.sh" --dry-run "$name" | sed -n 's/^BRANCH_NAME: //p')
[ -n "$branch" ] || { echo "create-new-feature.sh BRANCH_NAME vermedi" >&2; exit 1; }

git -C "$impl" switch -c "$branch"

echo $branch