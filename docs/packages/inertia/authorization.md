Source: https://inertiajs.com/docs/v3/security/authorization.md

# Authorization

When using Inertia, authorization is best handled server-side in your application's authorization policies. You may still need to perform authorization checks in your Inertia page components, where your framework's server-side helpers are unavailable.

The simplest approach is to pass the results of your authorization checks directly to your page components as props.

```php theme={null}
class UsersController extends Controller
{
    public function index()
    {
        return Inertia::render('Users/Index', [
            'can' => [
                'create_user' => Auth::user()->can('create', User::class),
            ],
            'users' => User::all()->map(function ($user) {
                return [
                    'first_name' => $user->first_name,
                    'last_name' => $user->last_name,
                    'email' => $user->email,
                    'can' => [
                        'edit_user' => Auth::user()->can('edit', $user),
                    ]
                ];
            }),
        ]);
    }
}
```
