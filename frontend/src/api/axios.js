import axios from 'axios';

// CSRFトークンをCookieから取得する関数
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // このCookie文字列が名前文字列で始まるか？
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Configures axios to send cookies
});

// リクエストインターセプター: CSRFトークンをヘッダーに付与
api.interceptors.request.use((config) => {
    // CSRFトークンが必要なメソッドの場合
    if (['post', 'put', 'delete', 'patch'].includes(config.method)) {
        const csrfToken = getCookie('csrf_access_token'); // flask-jwt-extendedのデフォルト設定名を確認する必要あり
        // Flask側で `app.config["JWT_COOKIE_CSRF_PROTECT"] = True` の場合
        // デフォルトでは `csrf_access_token` という名前のCookieにトークンが入るが、
        // フロントエンドから送信するヘッダー名は `X-CSRF-TOKEN` が一般的。

        // バックエンドのコードを確認すると:
        // api.spec.components.security_scheme("csrfToken", {"name": "X-CSRF-TOKEN", ...})
        // とあるので、ヘッダー名は X-CSRF-TOKEN で正しい。
        // Cookie名は flask-jwt-extended のデフォルトだと `csrf_access_token`
        if (csrfToken) {
            config.headers['X-CSRF-TOKEN'] = csrfToken;
        }
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;
