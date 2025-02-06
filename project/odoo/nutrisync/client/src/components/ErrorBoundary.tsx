import React from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";

interface Props {
  children?: React.ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle className="text-destructive">Something went wrong</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                An error occurred while rendering this page. Please try reloading.
              </p>
              {this.state.error && (
                <pre className="mt-4 p-4 bg-muted rounded-lg text-sm overflow-auto">
                  {this.state.error.message}
                </pre>
              )}
            </CardContent>
            <CardFooter>
              <Button onClick={this.handleReload}>Reload Page</Button>
            </CardFooter>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}