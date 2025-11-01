function app() {
    return {
        token: localStorage.getItem('token'),
        refreshToken: localStorage.getItem('refreshToken'),
        isAdmin: false,
        cars: [],
        users: [],
        showLoginModal: false,
        showRegisterModal: false,
        showCarModal: false,
        loginForm: {
            email: '',
            password: ''
        },
        registerForm: {
            email: '',
            password: ''
        },
        carForm: {
            id: null,
            model: '',
            store_id: ''
        },

        init() {
            if (this.token) {
                this.fetchCars();
                this.checkAdmin();
            }
        },

        // Authentication
        async login() {
            try {
                console.log('Attempting login with:', this.loginForm);
                const response = await axios.post('http://127.0.0.1:5000/login', this.loginForm);
                console.log('Login response:', response.data);
                this.token = response.data.access_token;
                this.refreshToken = response.data.refresh_token;
                localStorage.setItem('token', this.token);
                localStorage.setItem('refreshToken', this.refreshToken);
                this.showLoginModal = false;
                await this.checkAdmin();
                alert('Login successful!');
            } catch (error) {
                console.error('Login error:', error.response?.data || error);
                alert(error.response?.data?.error || 'Login failed. Please check your credentials.');
            }
        },

        async register() {
            try {
                console.log('Attempting registration with:', {
                    email: this.registerForm.email,
                    password: this.registerForm.password,
                    role: 'admin'
                });
                const response = await axios.post('http://127.0.0.1:5000/registry', {
                    email: this.registerForm.email,
                    password: this.registerForm.password,
                    role: 'admin'  // Set role as admin for testing
                });
                console.log('Registration response:', response.data);
                this.showRegisterModal = false;
                this.loginForm = { ...this.registerForm };
                this.showLoginModal = true;
                alert('Registration successful! Please login.');
            } catch (error) {
                console.error('Registration error:', error.response?.data || error);
                alert(error.response?.data?.error || 'Registration failed. Please try again.');
            }
        },

        logout() {
            this.token = null;
            this.refreshToken = null;
            this.isAdmin = false;
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            this.cars = [];
            this.users = [];
        },

        async refreshAuthToken() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/refresh', {}, {
                    headers: { 'Authorization': `Bearer ${this.refreshToken}` }
                });
                this.token = response.data.access_token;
                localStorage.setItem('token', this.token);
                return true;
            } catch (error) {
                this.logout();
                return false;
            }
        },

        // Cars Management
        async fetchCars() {
            if (!this.isAdmin) return; // Only admin can fetch cars
            try {
                const response = await axios.get('http://127.0.0.1:5000/cars', {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                });
                this.cars = response.data;
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const refreshed = await this.refreshAuthToken();
                    if (refreshed) this.fetchCars();
                } else if (error.response && error.response.status === 403) {
                    console.log('Access denied: Admin rights required');
                } else {
                    console.error('Error fetching cars:', error);
                }
            }
        },

        async saveCar() {
            try {
                if (this.carForm.id) {
                    await axios.put(`http://127.0.0.1:5000/cars/${this.carForm.id}`, {
                        model: this.carForm.model,
                        store_id: this.carForm.store_id
                    }, {
                        headers: { 'Authorization': `Bearer ${this.token}` }
                    });
                } else {
                    await axios.post('http://127.0.0.1:5000/cars', {
                        model: this.carForm.model,
                        store_id: this.carForm.store_id
                    }, {
                        headers: { 'Authorization': `Bearer ${this.token}` }
                    });
                }
                this.showCarModal = false;
                this.carForm = { id: null, model: '', store_id: '' };
                this.fetchCars();
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const refreshed = await this.refreshAuthToken();
                    if (refreshed) this.saveCar();
                } else {
                    alert('Failed to save car. Please try again.');
                }
            }
        },

        async deleteCar(id) {
            if (!confirm('Are you sure you want to delete this car?')) return;
            
            try {
                await axios.delete(`http://127.0.0.1:5000/cars/${id}`, {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                });
                this.fetchCars();
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const refreshed = await this.refreshAuthToken();
                    if (refreshed) this.deleteCar(id);
                } else {
                    alert('Failed to delete car. Please try again.');
                }
            }
        },

        editCar(car) {
            this.carForm = { ...car };
            this.showCarModal = true;
        },

        // Admin Functions
        async checkAdmin() {
            try {
                // First, try to get users list which requires admin role
                const response = await axios.get('http://127.0.0.1:5000/users', {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                });
                this.isAdmin = true;
                this.users = response.data;
                
                // If we got here, user is admin, so fetch cars too
                this.fetchCars();
            } catch (error) {
                console.log('User is not admin:', error);
                this.isAdmin = false;
            }
        },

        async deleteUser(id) {
            if (!confirm('Are you sure you want to delete this user?')) return;
            
            try {
                await axios.delete(`http://127.0.0.1:5000/users/${id}`, {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                });
                this.checkAdmin();
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const refreshed = await this.refreshAuthToken();
                    if (refreshed) this.deleteUser(id);
                } else {
                    alert('Failed to delete user. Please try again.');
                }
            }
        },

        async editUser(user) {
            // Implement user editing functionality if needed
        }
    }
}