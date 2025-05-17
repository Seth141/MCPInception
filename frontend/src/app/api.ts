import axios, { AxiosError, AxiosProgressEvent, AxiosRequestConfig, CancelTokenSource } from 'axios';
import { saveAs } from 'file-saver';

// Request interfaces
export interface GenerateRequest {
  url: string;
  options?: McpGenerationOptions;
}

export interface McpGenerationOptions {
  includeReadme?: boolean;
  customServerName?: string;
  timeout?: number; // in milliseconds
}

// Response interfaces
export interface ErrorResponse {
  detail: string;
  code?: string;
  status?: number;
}

export interface ProgressInfo {
  stage: 'scraping' | 'parsing' | 'generating' | 'downloading';
  percent: number;
  message?: string;
}

// Configuration
const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend
const DEFAULT_TIMEOUT = 60000; // 60 seconds
const DEFAULT_RETRY_ATTEMPTS = 2;
const DEFAULT_RETRY_DELAY = 1000; // 1 second

/**
 * Generates an MCP server based on the provided website URL
 * 
 * @param url - The URL of the website to generate an MCP server for
 * @param options - Additional options for the generation process
 * @param onProgress - Optional callback for tracking generation progress
 * @param abortSignal - Optional AbortSignal for cancelling the request
 * @returns A promise that resolves when the MCP server is generated and downloaded
 */
export async function generateMcpServer(
  url: string, 
  options?: McpGenerationOptions,
  onProgress?: (progress: ProgressInfo) => void,
  abortSignal?: AbortSignal
): Promise<void> {
  const source = axios.CancelToken.source();
  
  // Set up abort signal handler
  if (abortSignal) {
    abortSignal.addEventListener('abort', () => {
      source.cancel('Operation cancelled by user');
    });
  }
  
  // Configure request
  const requestConfig: AxiosRequestConfig = {
    responseType: 'blob',
    cancelToken: source.token,
    timeout: options?.timeout || DEFAULT_TIMEOUT,
    onDownloadProgress: (progressEvent: AxiosProgressEvent) => {
      if (onProgress && progressEvent.total) {
        onProgress({
          stage: 'downloading',
          percent: Math.round((progressEvent.loaded * 100) / progressEvent.total),
          message: 'Downloading MCP server package'
        });
      }
    }
  };

  try {
    // Report initial progress
    onProgress?.({ 
      stage: 'scraping', 
      percent: 0, 
      message: 'Starting API scraping process' 
    });

    // Make the request
    const response = await retryRequest(
      () => axios.post(
        `${API_BASE_URL}/generate`,
        { url, options } as GenerateRequest,
        requestConfig
      ),
      DEFAULT_RETRY_ATTEMPTS,
      DEFAULT_RETRY_DELAY,
      onProgress
    );

    // Download the zip file
    const filename = options?.customServerName 
      ? `${options.customServerName}.zip` 
      : 'mcp_server.zip';
    
    const blob = new Blob([response.data], { type: 'application/zip' });
    saveAs(blob, filename);
    
    // Report completion
    onProgress?.({ 
      stage: 'downloading', 
      percent: 100, 
      message: 'MCP server package downloaded successfully' 
    });
    
  } catch (error) {
    // Handle cancellation
    if (axios.isCancel(error)) {
      throw new Error('MCP server generation was cancelled');
    }
    
    // Handle network errors
    const axiosError = error as AxiosError<ErrorResponse>;
    if (axiosError.response) {
      // The server responded with an error status
      let errorDetail = 'Unknown server error';
      
      try {
        // Try to parse the error detail from the blob response
        if (axiosError.response.data instanceof Blob) {
          const text = await axiosError.response.data.text();
          const errorData = JSON.parse(text) as ErrorResponse;
          errorDetail = errorData.detail || errorDetail;
        } else if (typeof axiosError.response.data === 'object') {
          errorDetail = axiosError.response.data?.detail || errorDetail;
        }
      } catch (_) {
        // If parsing fails, use status text
        errorDetail = axiosError.response.statusText || errorDetail;
      }
      
      throw new Error(`Server error: ${errorDetail}`);
    } else if (axiosError.request) {
      // The request was made but no response was received
      throw new Error('No response from server. Please check your connection or try again later.');
    } else {
      // Something happened in setting up the request
      throw new Error(axiosError.message || 'Failed to generate MCP server');
    }
  }
}

/**
 * Helper function that implements retry logic for failed requests
 */
async function retryRequest(
  requestFn: () => Promise<any>,
  maxRetries: number, 
  delayMs: number,
  onProgress?: (progress: ProgressInfo) => void
): Promise<any> {
  let lastError: Error | null = null;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      // Report retry attempt if not the first try
      if (attempt > 0 && onProgress) {
        onProgress({
          stage: 'scraping',
          percent: 10,
          message: `Retrying (attempt ${attempt}/${maxRetries})...`
        });
      }
      
      return await requestFn();
    } catch (error) {
      lastError = error as Error;
      
      // Don't retry if it's a cancellation or a 4xx error
      if (axios.isCancel(error)) {
        throw error;
      }
      
      const axiosError = error as AxiosError;
      if (axiosError.response && axiosError.response.status >= 400 && axiosError.response.status < 500) {
        throw error;
      }
      
      // Last attempt, don't delay just throw
      if (attempt === maxRetries) {
        throw error;
      }
      
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  
  // This should never happen due to the throw in the loop
  throw lastError || new Error('Unknown error during request retry');
}

/**
 * Checks if the server is reachable and ready to accept requests
 * @returns A promise that resolves to true if the server is available
 */
export async function checkServerAvailability(): Promise<boolean> {
  try {
    await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Utility to get a formatted error message from any error object
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}