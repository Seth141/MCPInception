import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Get query parameters from the incoming request
    const url = request.nextUrl.searchParams.get('url');
    const serverName = request.nextUrl.searchParams.get('serverName');
    
    // Build API URL with query parameters
    const apiUrl = new URL('http://localhost:8000/scraper');
    if (url) {
      apiUrl.searchParams.append('url', url);
    }
    if (serverName) {
      apiUrl.searchParams.append('serverName', serverName);
    }
    
    console.log('Proxying request to:', apiUrl.toString());
    
    // Make the fetch request to the backend
    const response = await fetch(apiUrl.toString(), {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }
    
    // Get the response data
    const data = await response.json();
    
    // Return the response data
    return NextResponse.json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'An unknown error occurred' },
      { status: 500 }
    );
  }
} 