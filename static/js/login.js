function login() {
    return {
        email: '',
        password: '',
        signInBtn: true,
        showPassword: false,
        loginSuccess: true,
        burgerMenu: false,

        toggleForm(isSignIn) {
            this.signInBtn = isSignIn;
        },

        getFormClass(isSignIn) {
            return this.signInBtn === isSignIn ? 'text-yellow' : 'text-white';
        },

        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        },

        getPasswordFieldType() {
            return this.showPassword ? 'text' : 'password';
        },

        getPasswordIconClass() {
            return this.showPassword ? 'fill-yellow' : '';
        },

        toggleBurgerMenu() {
            this.burgerMenu = !this.burgerMenu;
        },

        getBurgerClass(burgerMenu) {
            return burgerMenu ? '' : 'hidden';
        },

        googleAuth() {
            window.location.href = '/auth/google'
        },

        async submitForm(endpoint) {
            try {
                const response = await fetch(`/${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                    }),
                });

                if (response.status === 200 || response.status === 201) {
                    window.location.href = '/dashboard';
                } else {
                    this.loginSuccess = false;
                    setTimeout(() => this.loginSuccess = true, 5000)
                }
            } catch (error) {
                this.loginSuccess = false;
                setTimeout(() => this.loginSuccess = true, 5000)
            }
        }
    };
}
