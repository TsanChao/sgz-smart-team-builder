#!/bin/bash
# GitHub推送脚本 (SSH方式)

# 设置远程仓库URL（使用SSH方式）
git remote set-url origin git@github.com:TsanChao/sgz-smart-team-builder.git

# 推送到远程仓库
git push origin main