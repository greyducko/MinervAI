resource "aws_iam_openid_connect_provider" "this" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.this.arn]
    }
    
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:greyducko/MinervAI:ref:refs/heads/main"]
    }
  }
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid    = "AllowAssumeCDKBootstrapRoles"
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    resources = [
      "arn:aws:iam::${var.account_id}:role/cdk-hnb659fds-*"
    ]
  }
}

resource "aws_iam_role" "this" {
  name               = "github-actions-oidc-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "this" {
  name   = "github-actions-cdk-policy"
  role   = aws_iam_role.this.id
  policy = data.aws_iam_policy_document.policy.json
}