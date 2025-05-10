import os
import sys
import json
import re
import glob
import shutil
from pathlib import Path

def find_frontend_directory():
    """查找前端源代码目录"""
    # 常见的前端目录名称
    common_frontend_dirs = ['src', 'frontend', 'client', 'web', 'ui']
    
    # 首先检查当前目录
    current_dir = os.getcwd()
    for dir_name in common_frontend_dirs:
        if os.path.isdir(os.path.join(current_dir, dir_name)):
            # 确保这是一个前端目录，检查是否包含package.json或index.html
            potential_dir = os.path.join(current_dir, dir_name)
            if (os.path.exists(os.path.join(current_dir, 'package.json')) or 
                os.path.exists(os.path.join(potential_dir, 'package.json')) or
                os.path.exists(os.path.join(potential_dir, 'index.html'))):
                return potential_dir
    
    # 如果在当前目录没找到，向上一级查找
    parent_dir = os.path.dirname(current_dir)
    if parent_dir != current_dir:  # 防止无限循环
        for dir_name in common_frontend_dirs:
            if os.path.isdir(os.path.join(parent_dir, dir_name)):
                potential_dir = os.path.join(parent_dir, dir_name)
                if (os.path.exists(os.path.join(parent_dir, 'package.json')) or 
                    os.path.exists(os.path.join(potential_dir, 'package.json')) or
                    os.path.exists(os.path.join(potential_dir, 'index.html'))):
                    return potential_dir
    
    # 搜索整个项目目录
    for root, dirs, files in os.walk(current_dir):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')  # 跳过node_modules目录
        if '.git' in dirs:
            dirs.remove('.git')  # 跳过.git目录
        
        # 检查是否是前端目录
        if 'package.json' in files or 'index.html' in files:
            # 找到src目录
            for dir_name in common_frontend_dirs:
                if dir_name in dirs:
                    return os.path.join(root, dir_name)
            # 如果没有找到常见目录，但有package.json，则返回当前目录
            return root
    
    # 如果以上方法都没找到，搜索API相关文件
    api_files = []
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.js') or file.endswith('.ts'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'axios' in content or 'fetch(' in content or '/api/' in content:
                            api_files.append(file_path)
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {str(e)}")
    
    if api_files:
        # 返回包含API相关文件最多的目录
        dirs_count = {}
        for file_path in api_files:
            dir_path = os.path.dirname(file_path)
            dirs_count[dir_path] = dirs_count.get(dir_path, 0) + 1
        
        # 按API文件数量排序
        sorted_dirs = sorted(dirs_count.items(), key=lambda x: x[1], reverse=True)
        print(f"根据API文件找到可能的前端目录: {sorted_dirs[0][0]}")
        return sorted_dirs[0][0]
    
    print("无法找到前端目录，请手动指定前端源代码目录")
    return None

def find_api_config_file(frontend_dir):
    """查找API配置文件"""
    # 常见的API配置文件路径
    common_api_paths = [
        'api/index.js', 'api/api.js', 'services/api.js', 'utils/api.js',
        'api/index.ts', 'api/api.ts', 'services/api.ts', 'utils/api.ts',
        'config/api.js', 'config/api.ts'
    ]
    
    for path in common_api_paths:
        full_path = os.path.join(frontend_dir, path)
        if os.path.exists(full_path):
            return full_path
    
    # 如果常见路径没找到，搜索包含axios或fetch的文件
    api_files = []
    for root, _, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith('.js') or file.endswith('.ts'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'axios' in content or 'fetch(' in content or '/api/' in content:
                            api_files.append(file_path)
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {str(e)}")
    
    if api_files:
        # 按文件中包含API调用的次数排序
        api_files_count = []
        for file_path in api_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    api_count = content.count('/api/') + content.count('axios') + content.count('fetch(')
                    api_files_count.append((file_path, api_count))
            except Exception as e:
                print(f"分析文件 {file_path} 时出错: {str(e)}")
        
        # 按API调用次数排序
        sorted_api_files = sorted(api_files_count, key=lambda x: x[1], reverse=True)
        if sorted_api_files:
            print(f"找到可能的API配置文件: {sorted_api_files[0][0]}")
            return sorted_api_files[0][0]
    
    print("无法找到API配置文件")
    return None

def fix_api_config_file(api_config_file):
    """修复API配置文件"""
    if not api_config_file or not os.path.exists(api_config_file):
        print("API配置文件不存在")
        return False
    
    # 备份原文件
    backup_file = api_config_file + '.bak'
    shutil.copy2(api_config_file, backup_file)
    print(f"原API配置文件已备份到: {backup_file}")
    
    try:
        with open(api_config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找baseURL配置
        base_url_pattern = re.compile(r'baseURL[\'"]?\s*:[\s\'"]([^\'",}]+)')
        base_url_match = base_url_pattern.search(content)
        
        if base_url_match:
            old_base_url = base_url_match.group(1).strip()
            print(f"找到当前baseURL: {old_base_url}")
            
            # 检查baseURL是否需要修改
            if old_base_url not in ['/api', 'http://localhost:5000/api']:
                # 替换baseURL
                new_content = base_url_pattern.sub(r'baseURL: "/api"', content)
                
                # 写入修改后的内容
                with open(api_config_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"已更新baseURL为: /api")
                return True
            else:
                print("baseURL已经是/api，无需修改")
                return True
        else:
            print("未找到baseURL配置，尝试添加")
            
            # 查找axios创建实例的地方
            axios_pattern = re.compile(r'(axios\.create\(\s*\{)')
            axios_match = axios_pattern.search(content)
            
            if axios_match:
                # 在axios.create中添加baseURL
                new_content = content.replace(
                    axios_match.group(1),
                    f"{axios_match.group(1)}\n  baseURL: '/api',"
                )
                
                # 写入修改后的内容
                with open(api_config_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("已添加baseURL: /api")
                return True
            else:
                print("未找到axios.create，无法添加baseURL")
                return False
    
    except Exception as e:
        print(f"修复API配置文件时出错: {str(e)}")
        # 恢复备份
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, api_config_file)
            print("已恢复原API配置文件")
        return False

def create_vite_config(frontend_dir):
    """创建或修改Vite配置文件，添加代理设置"""
    try:
        vite_config_file = None
        # 寻找vite.config.js或vite.config.ts
        for config_name in ['vite.config.js', 'vite.config.ts']:
            potential_config = os.path.join(Path(frontend_dir).parent, config_name)
            if os.path.exists(potential_config):
                vite_config_file = potential_config
                break
        
        if not vite_config_file:
            # 尝试在上级目录查找
            for config_name in ['vite.config.js', 'vite.config.ts']:
                potential_config = os.path.join(Path(frontend_dir).parent.parent, config_name)
                if os.path.exists(potential_config):
                    vite_config_file = potential_config
                    break
        
        if vite_config_file:
            print(f"找到Vite配置文件: {vite_config_file}")
            
            # 备份原文件
            backup_file = vite_config_file + '.bak'
            shutil.copy2(vite_config_file, backup_file)
            print(f"原Vite配置文件已备份到: {backup_file}")
            
            with open(vite_config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经配置了代理
            if 'proxy' in content and '/api' in content:
                print("Vite配置已包含API代理设置，无需修改")
                return True
            
            # 添加代理配置
            if 'export default defineConfig' in content:
                # 查找defineConfig配置对象
                if '{' in content:
                    if 'server' in content and 'server:' in content:
                        # 已有server配置，添加proxy
                        if 'server: {' in content:
                            new_content = content.replace(
                                'server: {',
                                '''server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false
    }
  },'''
                            )
                        else:
                            print("无法在server配置中添加proxy，请手动配置")
                            return False
                    else:
                        # 添加server配置
                        new_content = content.replace(
                            'export default defineConfig({',
                            '''export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  },'''
                        )
                    
                    # 写入修改后的内容
                    with open(vite_config_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print("已添加Vite API代理配置")
                    return True
                else:
                    print("无法解析Vite配置文件结构，请手动配置")
                    return False
            else:
                print("未找到defineConfig配置，请手动配置")
                return False
        else:
            print("未找到Vite配置文件，将创建新的配置文件")
            
            # 创建新的vite.config.js
            vite_config_file = os.path.join(Path(frontend_dir).parent, 'vite.config.js')
            vite_config_content = '''import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
});
'''
            with open(vite_config_file, 'w', encoding='utf-8') as f:
                f.write(vite_config_content)
            
            print(f"已创建新的Vite配置文件: {vite_config_file}")
            return True
    
    except Exception as e:
        print(f"配置Vite代理时出错: {str(e)}")
        # 恢复备份
        if vite_config_file and os.path.exists(backup_file):
            shutil.copy2(backup_file, vite_config_file)
            print("已恢复原Vite配置文件")
        return False

def get_frontend_port():
    """获取前端运行的端口号"""
    # 尝试在package.json中找dev脚本指定的端口
    if os.path.exists('package.json'):
        try:
            with open('package.json', 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                if 'scripts' in package_data and 'dev' in package_data['scripts']:
                    dev_script = package_data['scripts']['dev']
                    port_match = re.search(r'--port\s+(\d+)', dev_script)
                    if port_match:
                        return port_match.group(1)
        except Exception as e:
            print(f"读取package.json时出错: {str(e)}")
    
    # 默认值
    return 5173

def main():
    print("="*60)
    print("      银行客户画像系统前端配置修复工具")
    print("="*60)
    
    print("\n正在查找前端目录...")
    frontend_dir = find_frontend_directory()
    
    if frontend_dir:
        print(f"找到前端目录: {frontend_dir}")
        
        print("\n正在查找API配置文件...")
        api_config_file = find_api_config_file(frontend_dir)
        
        if api_config_file:
            print(f"找到API配置文件: {api_config_file}")
            
            print("\n正在修复API配置...")
            if fix_api_config_file(api_config_file):
                print("API配置修复完成")
            else:
                print("API配置修复失败")
        
        print("\n正在配置Vite代理...")
        if create_vite_config(frontend_dir):
            print("Vite代理配置完成")
        else:
            print("Vite代理配置失败")
        
        frontend_port = get_frontend_port()
        
        print("\n前端配置修复完成！")
        print("\n您现在可以使用以下命令启动应用：")
        print("\n1. 启动后端API服务:")
        print("   python apply_fixes.py")
        print("\n2. 启动前端开发服务:")
        print("   npm run dev")
        print(f"\n前端将运行在: http://localhost:{frontend_port}")
        print("后端API将运行在: http://localhost:5000")
        print("\n如果您的前端正确配置了API代理，前端请求将被代理到后端。")
        print("如果遇到跨域问题，请确保后端已启用CORS。")
        print("\n您可以使用以下测试账号登录系统:")
        print("- 管理员: admin / admin123")
        print("- 客户经理: manager1 / 123456")
        print("- 客户: customer1 / 123456")
    else:
        print("未找到前端目录，请手动配置")
    
    print("="*60)

if __name__ == "__main__":
    main() 