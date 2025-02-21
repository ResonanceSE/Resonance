export default defineNuxtRouteMiddleware((to) => {
    const token = useCookie<string | null>('token').value;
    if (!token && to.path !== '/login') {
      return navigateTo('/login');
    }
  });
  