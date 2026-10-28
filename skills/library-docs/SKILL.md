---
name: library-docs
description: Check current, version-specific library documentation before writing or changing code that uses a third-party library, SDK, framework or tool (for example AWS SDK v3, Node.js, Express, Sequelize, .NET, Angular, React, Terraform providers, Kubernetes, Helm, Datadog). Uses Context7 when its MCP tools are available, otherwise the official docs on the web. Use this whenever the user asks for code, config, setup steps, upgrades or migrations involving a named library or version, says "use context7", "check the docs" or "library-docs", or when an API might have changed since training, even if they don't ask for a docs check.
---

# Library docs check

Models often remember older versions of libraries, so they invent options, use removed APIs or mix versions. This skill makes you look up the current docs for the exact version first, then write code that matches them, and say what you checked.

## 1. Find the library and version

- Work out which libraries the task touches.
- Find the version actually in use, in this order: the user's message; project files if you can read them (`package.json` and the lock file, `*.csproj` or `Directory.Packages.props`, `requirements.txt` or `pyproject.toml`, `go.mod`, `.terraform.lock.hcl`, `Chart.yaml`); otherwise assume the latest stable release and say so.
- If two libraries interact (for example the AWS SDK v3 S3 client and its presigner package), check both.

## 2. Look it up

**If Context7 MCP tools are available** (names like `resolve-library-id` and `query-docs`; older versions call the second one `get-library-docs`):

1. Call `resolve-library-id` with the library name. If the user gave a Context7 id such as `/vercel/next.js` or `/vercel/next.js/v15.1.0`, use it directly.
2. Pick the best match: the official repository, the right major version, good documentation coverage.
3. Call `query-docs` (or `get-library-docs`) with that id and a focused topic, such as "presigned upload URL" rather than the whole library. Ask for more only if the first answer doesn't cover the task.

**If Context7 isn't available but web search is:** search for the official documentation for that library and version (vendor docs, the project's own site or repository, release notes or migration guide), and open the most relevant page. Prefer official sources over blogs and forum answers.

**If neither is available:** say that you couldn't check the live docs, write the code from what you know, and flag the parts most likely to have changed so the user can verify them.

## 3. Keep company data out of the lookup

Lookups go to outside services. Only send library names, versions and generic technical topics. Never include company code, internal names, hostnames, credentials, customer data, ticket contents or error messages containing any of those. Rephrase the question generically, for example "Sequelize transaction with row lock" rather than pasting the failing query.

## 4. Write the answer

- Use only the APIs, options and patterns that the docs you checked show for that version.
- If the docs contradict what you would have written from memory, follow the docs, and mention the difference briefly when it matters (for example "v3 uses `send(new PutObjectCommand(...))`, not `s3.putObject().promise()`").
- If something isn't covered by the docs you found, say so rather than guessing.
- Start the answer with one short line saying what you checked:

  `Docs checked: @aws-sdk/client-s3 v3 and @aws-sdk/s3-request-presigner (Context7, /aws/aws-sdk-js-v3)`

  or, after a web search:

  `Docs checked: Terraform AWS provider 6.x, aws_s3_bucket_lifecycle_configuration (registry.terraform.io)`

## Examples

**Example 1**
User: "Write a function to create a presigned S3 upload URL in Node."
Do: check `@aws-sdk/client-s3` and `@aws-sdk/s3-request-presigner` (v3), then use `PutObjectCommand` with `getSignedUrl`, and set an expiry.

**Example 2**
User: "Add an S3 lifecycle rule in Terraform to move logs to Glacier after 30 days."
Do: check the AWS provider docs for `aws_s3_bucket_lifecycle_configuration`, since lifecycle rules moved out of the `aws_s3_bucket` resource in provider v4. Write it with the separate resource.

**Example 3**
User: "use context7 — how do I do a managed transaction with a row lock in Sequelize?"
Do: resolve Sequelize, query "transactions" and "locking" for the user's version, and show the managed transaction with `lock: t.LOCK.UPDATE`, passing `transaction: t` to every query inside it.
