# Enforcing EC2 Tagging Policy in AWS for Cost and Resource Management

This project demonstrates how to enforce tagging policies on EC2 instances in AWS to improve cost visibility, resource accountability, and operational governance.

As part of a personal learning exercise, I implemented tag enforcement using AWS IAM policies. This approach ensures that users cannot launch EC2 instances without applying required metadata through tags.

## Objective

The goal is to prevent EC2 instance launches unless the following tags are provided:

- `Email`: Identifies the owner; must follow a specific domain pattern.
- `Team`: Indicates the team using the resource (e.g., DevOps, Backend, Frontend).
- `Place`: Specifies location or deployment region (e.g., Mumbai).
- `Name`: A logical name for the instance (optional value, but key must be present).

Tag enforcement like this helps with:

- Identifying who launched a resource.
- Understanding the purpose and ownership of resources.
- Enabling more accurate cost allocation and budget tracking.

## IAM Policy-Based Tag Enforcement

A custom IAM policy named `EC2-Tag-Enforcement` was created and attached to a user group called `Tag-Enf`. All relevant users who launch EC2 instances can be added to this group.

This policy enforces tag requirements at the time of resource creation using the `aws:RequestTag` and `aws:TagKeys` conditions.

## Example Policy Snippet

The policy was built using the IAM visual editor and includes the following conditions:

```json
"Condition": {
  "StringEquals": {
    "aws:RequestTag/Team": ["Backend", "DevOps", "Frontend"]
  },
  "StringLike": {
    "aws:RequestTag/Email": "*@example.com"
  },
  "ForAnyValue:StringEquals": {
    "aws:TagKeys": ["Email", "Name", "Place", "Team"]
  }
}
```

## Screenshots
![](screenshots/1751723052906.jpg)
![](screenshots/1751723052577.jpg)
![](screenshots/1751723052800.jpg)
