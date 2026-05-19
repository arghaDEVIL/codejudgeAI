# shadcn/ui Select Component Fix

## Issue
Error: `A <Select.Item /> must have a value prop that is not an empty string`

## Root Cause
The shadcn/ui Select component does not allow empty string values for SelectItem components. This is by design because the Select value can be set to an empty string to clear the selection and show the placeholder.

## Location
`frontend/src/pages/RoomLobby.jsx` - Problem selection dropdown in the "Create Room" form

## Fix Applied

### Before (Incorrect)
```jsx
<Select
    value={createForm.problem_id?.toString() || ''}
    onValueChange={(value) => setCreateForm({ ...createForm, problem_id: value ? parseInt(value) : null })}
>
    <SelectTrigger id="problem">
        <SelectValue placeholder="No problem - Free coding" />
    </SelectTrigger>
    <SelectContent>
        <SelectItem value="">No problem - Free coding</SelectItem>
        {problems.map((problem) => (
            <SelectItem key={problem.id} value={problem.id.toString()}>
                {problem.title} ({problem.difficulty})
            </SelectItem>
        ))}
    </SelectContent>
</Select>
```

### After (Correct)
```jsx
<Select
    value={createForm.problem_id?.toString() || 'none'}
    onValueChange={(value) => setCreateForm({ ...createForm, problem_id: value === 'none' ? null : parseInt(value) })}
>
    <SelectTrigger id="problem">
        <SelectValue placeholder="No problem - Free coding" />
    </SelectTrigger>
    <SelectContent>
        <SelectItem value="none">No problem - Free coding</SelectItem>
        {problems.map((problem) => (
            <SelectItem key={problem.id} value={problem.id.toString()}>
                {problem.title} ({problem.difficulty})
            </SelectItem>
        ))}
    </SelectContent>
</Select>
```

## Changes Made
1. Changed empty string `""` to `"none"` for the "No problem" option
2. Updated the default value fallback from `|| ''` to `|| 'none'`
3. Updated the onValueChange handler to check for `value === 'none'` instead of `value ? ... : null`

## Result
- ✅ No more Select component errors
- ✅ "No problem - Free coding" option works correctly
- ✅ Form submission properly handles null problem_id when "none" is selected
- ✅ All other problem selections work as expected

## Best Practice
When using shadcn/ui Select components:
- Never use empty strings `""` as SelectItem values
- Use meaningful string values like `"none"`, `"all"`, `"default"`, etc.
- Handle these special values in your onChange handlers
- Ensure default/fallback values are also non-empty strings
