# -*- coding: utf-8 -*-
import os, json, shutil, re, hashlib
from flask import Flask, render_template_string, request, redirect, url_for, session, send_from_directory

app = Flask(__name__)
app.secret_key = 'mingye-admin-2024'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = os.path.join(BASE_DIR, 'website')
UPLOAD_FOLDER = os.path.join(WEBSITE_DIR, 'images')
ADMIN_PASSWORD = 'admin123'

def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# 页面配置
PAGES = {
    'products.html': {'name': '产品分类页', 'url': '/products.html'},
    'products/series1.html': {'name': '系列1 - Beer Mugs', 'url': '/products/series1.html'},
    'products/series2.html': {'name': '系列2 - Whiskey', 'url': '/products/series2.html'},
    'products/series3.html': {'name': '系列3 - Bakeware', 'url': '/products/series3.html'},
    'products/series4.html': {'name': '系列4 - Cups', 'url': '/products/series4.html'},
}

# ======== 页面模板 ========
LOGIN_HTML = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Mingye Glass - 后台管理</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,sans-serif}
body{background:#f0f2f5;display:flex;min-height:100vh;align-items:center;justify-content:center}
.login-box{background:#fff;padding:40px;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.1);width:400px}
.login-box h1{text-align:center;color:#1a1a2e;margin-bottom:30px;font-size:22px}
input{width:100%;padding:12px 16px;border:2px solid #e0e0e0;border-radius:8px;font-size:15px;margin-bottom:16px}
input:focus{outline:none;border-color:#4a6cf7}
button{width:100%;padding:12px;background:#4a6cf7;color:#fff;border:none;border-radius:8px;font-size:16px;cursor:pointer}
button:hover{background:#3b5de7}
.error{color:#e74c3c;text-align:center;margin-bottom:12px}
</style></head><body>
<div class="login-box">
<h1>Mingye Glass 后台管理</h1>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
<form method="post">
<input type="password" name="password" placeholder="请输入管理员密码" required>
<button type="submit">登录</button>
</form></div></body></html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>后台管理</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,sans-serif}
body{background:#f0f2f5}
.header{background:#1a1a2e;color:#fff;padding:16px 32px;display:flex;align-items:center;justify-content:space-between}
.header h1{font-size:18px}
.header a{color:#fff;text-decoration:none;font-size:13px;opacity:.8}
.container{max-width:1200px;margin:0 auto;padding:24px}
.card{background:#fff;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.card h2{font-size:16px;color:#1a1a2e;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #eee}
.page-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.page-item{display:flex;align-items:center;justify-content:space-between;padding:16px;background:#f8f9fa;border-radius:8px;text-decoration:none;color:#333}
.page-item:hover{background:#e8ecf8}
.page-name{font-weight:600;font-size:14px}
.page-url{font-size:12px;color:#666;margin-top:4px}
.btn{display:inline-block;padding:8px 16px;border-radius:6px;text-decoration:none;font-size:13px;border:none;cursor:pointer}
.btn-primary{background:#4a6cf7;color:#fff}
.btn-primary:hover{background:#3b5de7}
.btn-sm{padding:6px 12px;font-size:12px}
.actions{display:flex;gap:8px;margin-top:20px}
.upload-area{border:2px dashed #ccc;border-radius:8px;padding:40px;text-align:center;margin:16px 0}
.upload-area.dragover{border-color:#4a6cf7;background:#f0f4ff}
.upload-btn{display:inline-block;padding:10px 24px;background:#4a6cf7;color:#fff;border-radius:6px;cursor:pointer;font-size:14px}
.upload-btn:hover{background:#3b5de7}
input[type="file"]{display:none}
.file-list{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.file-item{position:relative;width:120px;height:120px;border-radius:8px;overflow:hidden;border:1px solid #eee}
.file-item img{width:100%;height:100%;object-fit:cover}
.file-item .del{position:absolute;top:4px;right:4px;background:rgba(0,0,0,.6);color:#fff;border:none;border-radius:50%;width:22px;height:22px;cursor:pointer;font-size:12px;line-height:22px;text-align:center;text-decoration:none}
#message{position:fixed;top:20px;right:20px;padding:12px 24px;border-radius:8px;color:#fff;display:none;z-index:999}
#message.success{background:#27ae60;display:block}
#message.error{background:#e74c3c;display:block}
</style></head><body>
<div class="header"><h1>Mingye Glass 后台管理</h1><a href="/admin/logout">退出登录</a></div>
<div class="container">
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}{% for cat,msg in messages %}
<div id="message" class="{{ cat }}">{{ msg }}</div>{% endfor %}{% endif %}{% endwith %}

<div class="card">
<h2>页面管理</h2>
<div class="page-list">
{% for file,info in pages.items() %}
<a class="page-item" href="/admin/edit/{{ file }}">
<div><div class="page-name">{{ info.name }}</div><div class="page-url">{{ file }}</div></div>
<span style="color:#4a6cf7;font-size:13px">编辑 →</span>
</a>
{% endfor %}
</div></div>

<div class="card">
<h2>上传图片</h2>
<div class="upload-area" id="dropZone">
<p style="color:#999;margin-bottom:12px">拖拽图片到此处或点击选择</p>
<label class="upload-btn" for="fileInput">选择图片</label>
<input type="file" id="fileInput" multiple accept="image/*" onchange="uploadFiles(this.files)">
</div>
<div id="uploadStatus" style="margin-top:12px;font-size:13px;color:#666"></div>
<div class="file-list" id="fileList">{% for img in images %}<div class="file-item"><img src="/images/{{ img }}"><a class="del" href="/admin/delete-image/{{ img }}" onclick="return confirm('删除这张图片？')">×</a></div>{% endfor %}</div>
</div>

<div class="card">
<h2>快捷操作</h2>
<div class="actions">
<a href="/" class="btn btn-primary" target="_blank">查看网站</a>
<a href="/admin/refresh" class="btn btn-primary">刷新页面列表</a>
</div></div>
</div>
<script>
function uploadFiles(files){if(!files.length)return;var fd=new FormData();for(var f of files)fd.append('files',f);var st=document.getElementById('uploadStatus');st.textContent='上传中...';fetch('/admin/upload',{method:'POST',body:fd}).then(function(r){return r.json()}).then(function(d){if(d.success){st.textContent='上传成功！';setTimeout(function(){location.reload()},1000)}else{st.textContent='上传失败: '+d.error}}).catch(function(e){st.textContent='上传出错'})}
var dz=document.getElementById('dropZone');dz.addEventListener('dragover',function(e){e.preventDefault();dz.classList.add('dragover')});dz.addEventListener('dragleave',function(e){dz.classList.remove('dragover')});dz.addEventListener('drop',function(e){e.preventDefault();dz.classList.remove('dragover');uploadFiles(e.dataTransfer.files)});setTimeout(function(){var m=document.getElementById('message');if(m)setTimeout(function(){m.style.display='none'},3000)},500)
</script></body></html>
'''

EDIT_HTML = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>编辑页面</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,sans-serif}
body{background:#f0f2f5}
.header{background:#1a1a2e;color:#fff;padding:16px 32px;display:flex;align-items:center;gap:20px}
.header a{color:#fff;text-decoration:none;font-size:13px;opacity:.8}
.container{max-width:1200px;margin:0 auto;padding:24px}
.card{background:#fff;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.card h2{font-size:16px;color:#1a1a2e;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #eee}
textarea{width:100%;height:600px;padding:16px;border:2px solid #e0e0e0;border-radius:8px;font-size:13px;font-family:'Consolas','Courier New',monospace;line-height:1.6;resize:vertical}
textarea:focus{outline:none;border-color:#4a6cf7}
.btn{display:inline-block;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;border:none;cursor:pointer}
.btn-primary{background:#4a6cf7;color:#fff}
.btn-primary:hover{background:#3b5de7}
.btn-secondary{background:#666;color:#fff}
.actions{display:flex;gap:12px;margin-top:16px}
.form-group{margin-bottom:16px}
label{display:block;font-weight:600;margin-bottom:6px;font-size:14px}
input[type="text"]{width:100%;padding:10px 14px;border:2px solid #e0e0e0;border-radius:6px;font-size:14px}
#message{position:fixed;top:20px;right:20px;padding:12px 24px;border-radius:8px;color:#fff;display:none;z-index:999}
#message.success{background:#27ae60;display:block}
#message.error{background:#e74c3c;display:block}
</style></head><body>
<div class="header"><a href="/admin">← 返回后台</a><span style="font-size:16px">编辑: {{ page_name }}</span></div>
<div class="container">
<div class="card">
<form method="post" action="/admin/save/{{ page_file }}">
<div class="form-group"><label>HTML 源代码（直接编辑页面内容）</label>
<textarea name="content" spellcheck="false">{{ content }}</textarea></div>
<div class="actions">
<button type="submit" class="btn btn-primary">保存修改</button>
<a href="/{{ page_file }}" class="btn btn-secondary" target="_blank">预览页面</a>
</div></form></div></div>
<script>setTimeout(function(){var m=document.getElementById('message');if(m)setTimeout(function(){m.style.display='none'},3000)},500)</script></body></html>
'''

@app.route('/admin', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template_string(LOGIN_HTML, error='密码错误')
    return render_template_string(LOGIN_HTML, error=None)

@app.route('/admin/dashboard')
@login_required
def dashboard():
    images = sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.jpg','.png','.jpeg','.gif')) and not os.path.isdir(os.path.join(UPLOAD_FOLDER,f))])
    return render_template_string(DASHBOARD_HTML, pages=PAGES, images=images)

@app.route('/admin/edit/<path:page_file>')
@login_required
def edit_page(page_file):
    filepath = os.path.join(WEBSITE_DIR, page_file)
    if not os.path.exists(filepath):
        return '文件不存在', 404
    page_name = PAGES.get(page_file, {}).get('name', page_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template_string(EDIT_HTML, page_file=page_file, page_name=page_name, content=content)

@app.route('/admin/save/<path:page_file>', methods=['POST'])
@login_required
def save_page(page_file):
    filepath = os.path.join(WEBSITE_DIR, page_file)
    content = request.form.get('content', '')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    from flask import flash
    flash('保存成功！', 'success')
    return redirect(url_for('edit_page', page_file=page_file))

@app.route('/admin/upload', methods=['POST'])
@login_required
def upload():
    files = request.files.getlist('files')
    uploaded = []
    for f in files:
        if f.filename:
            safe_name = f.filename.replace(' ', '_').replace('(', '').replace(')', '')
            path = os.path.join(UPLOAD_FOLDER, safe_name)
            f.save(path)
            uploaded.append(safe_name)
    return {'success': True, 'files': uploaded}

@app.route('/admin/delete-image/<filename>')
@login_required
def delete_image(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    from flask import flash
    flash('图片已删除', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/refresh')
@login_required
def refresh():
    return redirect(url_for('dashboard'))

@app.route('/')
def index():
    return redirect(url_for('serve_static', filename='index.html'))

@app.route('/<path:filename>')
def serve_static(filename):
    safe_path = filename.replace('..', '').lstrip('/')
    filepath = os.path.join(WEBSITE_DIR, safe_path)
    if os.path.isfile(filepath):
        return send_from_directory(WEBSITE_DIR, safe_path)
    return '<h1>404 Not Found</h1>', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
