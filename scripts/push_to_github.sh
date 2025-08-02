#!/bin/bash
# GitHub推送脚本

# 设置远程仓库URL（使用环境变量）
git remote set-url origin https://TsanChao:${GITHUB_PAT}@github.com/TsanChao/sgz-smart-team-builder.git

# 推送到远程仓库
git push origin main