export const apiCall = async (url: string, options: RequestInit = {}) => {
  const accessToken = localStorage.getItem('access_token');
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status}`);
  }

  return response.json();
};

export const addToCart = async (variantId: string, quantity: number) => {
  return apiCall('http://127.0.0.1:8000/api/cart/add', {
    method: 'POST',
    body: JSON.stringify({ variant_id: variantId, quantity }),
  });
};

export const getCartItems = async () => {
  return apiCall('http://127.0.0.1:8000/api/cart');
};

export const getProducts = async () => {
  return apiCall('http://127.0.0.1:8000/api/tshirts');
}; 