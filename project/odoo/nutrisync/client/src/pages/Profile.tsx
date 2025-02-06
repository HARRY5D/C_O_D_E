import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { UserCircle, Mail, Phone, MapPin } from 'lucide-react';

export function Profile() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Profile</h1>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input id="name" type="text" defaultValue="John Doe" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" defaultValue="john@example.com" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Phone</Label>
                <Input id="phone" type="tel" defaultValue="+1 (555) 123-4567" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Input id="address" type="text" defaultValue="123 Main St, City, State" />
              </div>
              <Button type="submit">Save Changes</Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Account Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <UserCircle className="h-5 w-5 text-brand-500" />
              <div className="flex-1">
                <h3 className="font-medium">Profile Picture</h3>
                <p className="text-sm text-muted-foreground">Update your profile photo</p>
              </div>
              <Button variant="outline">Change</Button>
            </div>
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Mail className="h-5 w-5 text-brand-500" />
              <div className="flex-1">
                <h3 className="font-medium">Email Notifications</h3>
                <p className="text-sm text-muted-foreground">Manage email preferences</p>
              </div>
              <Button variant="outline">Configure</Button>
            </div>
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Phone className="h-5 w-5 text-brand-500" />
              <div className="flex-1">
                <h3 className="font-medium">Two-Factor Auth</h3>
                <p className="text-sm text-muted-foreground">Add extra security to your account</p>
              </div>
              <Button variant="outline">Enable</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}