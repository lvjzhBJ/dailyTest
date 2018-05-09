accessid = ''
accesskey = ''
host = ''
policyBase64 = ''
signature = ''
callbackbody = ''
filename = ''
key = ''
pjt_name = ''
expire = 0
g_object_name = ''
g_object_name_type = ''
now = timestamp = Date.parse(new Date()) / 1000;

function send_request(isPost)
{
    var xmlhttp = null;
    if (window.XMLHttpRequest)
    {
        xmlhttp=new XMLHttpRequest();
    } else if (window.ActiveXObject)
    {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    if (xmlhttp!=null) {
        if (true == isPost){
            serverUrl = '/pjt2db/';
            var form = new FormData();
            form.append('apk_file', apk_name);
            form.append('pjt_name', pjt_name);
            xmlhttp.open( "POST", serverUrl, true );
            xmlhttp.send( form );
            alert('上传过程请勿关闭浏览器...')
            return xmlhttp.responseText
        }else{
            serverUrl = '/get_oss_token/';
            xmlhttp.open( "GET", serverUrl, false );
            xmlhttp.send( null );
            return xmlhttp.responseText
        }

    } else {
        alert("Your browser does not support XMLHTTP.");
    }
};


// function check_object_radio() {
//     var tt = document.getElementsByName('myradio');
//     for (var i = 0; i < tt.length ; i++ )
//     {
//         if(tt[i].checked)
//         {
//             g_object_name_type = tt[i].value;
//             break;
//         }
//     }
// }

function get_signature()
{
    now = timestamp = Date.parse(new Date()) / 1000;
    if (expire < now + 3)
    {
        body = send_request(false)
        var obj = eval ("(" + body + ")");
        host = obj['host']
        policyBase64 = obj['policy']
        accessid = obj['accessid']
        signature = obj['signature']
        expire = parseInt(obj['expire'])
        callbackbody = obj['callback']
        key = obj['dir']
        return true;
    }
    return false;
};

// function random_string(len) {
// 　　len = len || 32;
// 　　var chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
// 　　var maxPos = chars.length;
// 　　var pwd = '';
// 　　for (i = 0; i < len; i++) {
//     　　pwd += chars.charAt(Math.floor(Math.random() * maxPos));
//     }
//     return pwd;
// }

// function get_suffix(filename) {
//     pos = filename.lastIndexOf('.')
//     suffix = ''
//     if (pos != -1) {
//         suffix = filename.substring(pos)
//     }
//     return suffix;
// }

function calculate_object_name(filename) {
//     if (g_object_name_type == 'local_name')
//     {
    g_object_name += "${filename}"
        // send_request(true);

//     }
//     else if (g_object_name_type == 'random_name')
//     {
//         suffix = get_suffix(filename)
//         g_object_name = key + random_string(10) + suffix
//     }
    return ''
}

// function get_uploaded_object_name(filename)
// {
//     if (g_object_name_type == 'local_name')
//     {
//         tmp_name = g_object_name
//         tmp_name = tmp_name.replace("${filename}", filename);
//         return tmp_name
//     }
//     else if(g_object_name_type == 'random_name')
//     {
//         return g_object_name
//     }
// }

function check_pjt_name() {
    return document.getElementById('id_pjt_name').value;
}

function set_upload_param(up, filename, ret) {
    if (ret == false) {
        ret = get_signature()
    }
    g_object_name = key;
    if (filename != '') {
        // suffix = get_suffix(filename)
        post_get = send_request(true);
        if (String(post_get).indexOf("dd_test_apk_") == -1){
                alert('上传服务器未及时响应，请稍后再试...')
        }else {
            g_object_name += post_get;
            calculate_object_name(filename)
        }
    }
    new_multipart_params = {
        'key' : g_object_name,
        'policy': policyBase64,
        'OSSAccessKeyId': accessid,
        'success_action_status' : '200', //让服务端返回200,不然，默认会返回204
        'callback' : callbackbody,
        'signature': signature,
    };

    up.setOption({
        'url': host,
        'multipart_params': new_multipart_params
    });
    up.start();
}

var uploader = new plupload.Uploader({
	runtimes : 'html5,flash,silverlight,html4',
	browse_button : 'selectfiles',
	container: document.getElementById('container'),
	flash_swf_url : 'lib/plupload-2.1.2/js/Moxie.swf',
	silverlight_xap_url : 'lib/plupload-2.1.2/js/Moxie.xap',
    url : 'http://oss.aliyuncs.com',

    filters: {
        mime_types : [ //只允许上传图片和zip,rar文件
            // { title : "Image files", extensions : "jpg,gif,png,bmp" },
            // { title : "Zip files", extensions : "zip,rar" }
            { title : "App Install files", extensions : "apk" }
        ],
        max_file_size : '400mb', //最大只能上传10mb的文件
        prevent_duplicates : true //不允许选取重复文件
    },

	init: {
		PostInit: function() {
			document.getElementById('ossfile').innerHTML = '';
			document.getElementById('postfiles').onclick = function() {
			    if (check_pjt_name()){
			        document.getElementById('console').innerHTML='';
			        pjt_name = document.getElementById('id_pjt_name').value;
                }else{
			        document.getElementById('console').innerHTML='<i class="layui-icon" style="font-size: 20px; color: #FF7200;">&#xe69c;   请输入项目名称</i>';
			        return false;
                }
                set_upload_param(uploader, '', false);
                return false;
			};
		},

		FilesAdded: function(up, files) {
			plupload.each(files, function(file) {
				document.getElementById('ossfile').innerHTML += '<div id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ')<b></b>'
				+'<div class="progress"><div class="progress-bar" style="width: 0%"></div></div>'
				+'</div>';
				apk_name = file.name
			});
		},

		BeforeUpload: function(up, file) {
            // check_object_radio();
            set_upload_param(up, file.name, true);
        },

		UploadProgress: function(up, file) {
			var d = document.getElementById(file.id);
			d.getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
            var prog = d.getElementsByTagName('div')[0];
			var progBar = prog.getElementsByTagName('div')[0]
			progBar.style.width= 2*file.percent+'px';
			progBar.setAttribute('aria-valuenow', file.percent);
		},

		FileUploaded: function(up, file, info) {
            if (info.status == 200) {
                document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = 'upload to oss success, object name:' + get_uploaded_object_name(file.name);
            } else {
                document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = info.response;
            }
		},

		Error: function(up, err) {
		    document.getElementById('console').innerText = ''
            if (err.code == -600) {
                document.getElementById('console').appendChild(document.createTextNode("\n选择的文件太大了,非会员限制400M"));
            } else if (err.code == -601) {
                document.getElementById('console').appendChild(document.createTextNode("\n选择文件格式不正确，目前支持apk文件"));
            } else if (err.code == -602) {
                document.getElementById('console').appendChild(document.createTextNode("\n已上传过，忽略..."));
            } else {
                document.getElementById('console').appendChild(document.createTextNode("\nError xml:" + err.response));
            }
		}
	}
});

uploader.init();
