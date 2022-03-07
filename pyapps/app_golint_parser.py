# coding: utf-8

import json
import os
import sys


def read_lint_issues(path: str) -> list:
    with open(path, mode='r') as f:
        lint_issues = []
        for line in f.readlines():
            if len(line.strip().strip('\n')) == 0:
                continue
            lint_results = json.loads(line)
            issues = lint_results['Issues']
            if issues and len(issues) > 0:
                lint_issues.extend(issues)
        return lint_issues


def format_issues(issues: list) -> list:
    ret_items = []
    for issue in issues:
        text = issue['Text']
        # filter
        if text.startswith('undeclared name'):
            continue
        pos = issue['Pos']
        item = {
            'Title': text,
            'Pos': f'{pos["Filename"]}:{pos["Line"]}:{pos["Column"]}',
            'Linter': issue['FromLinter'],
            'Code': issue['SourceLines'][0],
        }
        ret_items.append(item)
    return ret_items


def print_lint_summary(issues: list):
    res_dict = {}
    for issue in issues:
        print('%s\t%s' % (issue['Pos'], issue['Linter']))
        key = issue['Linter']
        res_dict[key] = res_dict.get(key, 0) + 1
    print()

    print('*' * 25, 'Golangci-Lint Summary')
    for k, v in res_dict.items():
        print(k, v)


def generate_lint_html_report(issues: list, path: str):
    html_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>golangci-lint</title>
    <link rel="shortcut icon" type="image/png" href="https://golangci-lint.run/favicon-32x32.png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.2/css/bulma.min.css"
          integrity="sha512-byErQdWdTqREz6DLAA9pCnLbdoGGhXfU6gm1c8bkf7F51JVmUBlayGe2A31VpXWQP+eiJ3ilTAZHCR3vmMyybA=="
          crossorigin="anonymous" referrerpolicy="no-referrer"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/styles/default.min.css"
          integrity="sha512-kZqGbhf9JTB4bVJ0G8HCkqmaPcRgo88F0dneK30yku5Y/dep7CZfCnNml2Je/sY4lBoqoksXz4PtVXS4GHSUzQ=="
          crossorigin="anonymous" referrerpolicy="no-referrer"/>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/highlight.min.js"
            integrity="sha512-s+tOYYcC3Jybgr9mVsdAxsRYlGNq4mlAurOrfNuGMQ/SCofNPu92tjE7YRZCsdEtWL1yGkqk15fU/ark206YTg=="
            crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/languages/go.min.js"
            integrity="sha512-+UYV2NyyynWEQcZ4sMTKmeppyV331gqvMOGZ61/dqc89Tn1H40lF05ACd03RSD9EWwGutNwKj256mIR8waEJBQ=="
            crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.production.min.js"
            integrity="sha512-qlzIeUtTg7eBpmEaS12NZgxz52YYZVF5myj89mjJEesBd/oE9UPsYOX2QAXzvOAZYEvQohKdcY8zKE02ifXDmA=="
            crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script type="text/javascript"
            src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.production.min.js"
            integrity="sha512-9jGNr5Piwe8nzLLYTk8QrEMPfjGU0px80GYzKZUxi7lmCfrBjtyCc1V5kkS5vxVwwIB7Qpzc7UxLiQxfAN30dw=="
            crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.26.0/babel.min.js"
            integrity="sha512-kp7YHLxuJDJcOzStgd6vtpxr4ZU9kjn77e6dBsivSz+pUuAuMlE2UTdKB7jjsWT84qbS8kdCWHPETnP/ctrFsA=="
            crossorigin="anonymous" referrerpolicy="no-referrer"></script>
</head>
<body>
<section class="section">
    <div class="container">
        <div id="content"></div>
    </div>
</section>
<script>
    const data = {{lint_issues}};
</script>
<script type="text/babel">
  class Highlight extends React.Component {
    componentDidMount() {
      hljs.highlightElement(ReactDOM.findDOMNode(this));
    }

    render() {
      return <pre className="go"><code>{this.props.code}</code></pre>;
    }
  }

  class Issue extends React.Component {
    render() {
      return (
        <div className="issue box">
          <div>
            <div className="columns">
              <div className="column is-four-fifths">
                <h5 className="title is-5 has-text-danger-dark">{this.props.data.Title}</h5>
              </div>
              <div className="column is-one-fifth">
                <h6 className="title is-6">{this.props.data.Linter}</h6>
              </div>
            </div>
            <strong>{this.props.data.Pos}</strong>
          </div>
          <div className="highlight">
            <Highlight code={this.props.data.Code}/>
          </div>
        </div>
      );
    }
  }

  class Issues extends React.Component {
    render() {
      if (!this.props.data.Issues || this.props.data.Issues.length === 0) {
        return (
          <div>
            <div className="notification">
              No issues found!
            </div>
          </div>
        );
      }

      return (
        <div className="issues">
          {this.props.data.Issues.map(issue => (<Issue data={issue}/>))}
        </div>
      );
    }
  }

  ReactDOM.render(
    <div className="content">
      <div className="columns is-centered">
        <div className="column is-three-quarters">
          <Issues data={data}/>
        </div>
      </div>
    </div>,
    document.getElementById("content")
  );
</script>
</body>
</html>
"""
    data = json.dumps({'Issues': issues})
    html = html_template.replace(r'{{lint_issues}}', data)

    if os.path.exists(path):
        os.remove(path)
    with open(path, mode='w') as f:
        f.write(html)


def create_test_data(path):
    # NOTE: should use "/t" in json string for tab.
    data = r"""
{"Issues":[{"FromLinter":"staticcheck","Text":"SA1029: should not use built-in type string as key for value; define your own type to avoid collisions","Severity":"","SourceLines":["\treturn context.WithValue(ctx, spbaMasterKey, tx)"],"Replacement":null,"Pos":{"Filename":"internal/manager/da/config.go","Offset":2787,"Line":62,"Column":32},"ExpectNoLint":false,"ExpectedNoLintLinter":""},{"FromLinter":"gosimple","Text":"S1000: should use for range instead of for { select {} }","Severity":"","SourceLines":["\tfor {"],"Replacement":null,"Pos":{"Filename":"internal/manager/da/config.go","Offset":4798,"Line":122,"Column":2},"ExpectNoLint":false,"ExpectedNoLintLinter":""}],"Report":{"Linters":[{"Name":"govet","Enabled":true,"EnabledByDefault":true},{"Name":"bodyclose"},{"Name":"noctx"},{"Name":"errcheck","Enabled":true,"EnabledByDefault":true},{"Name":"golint"},{"Name":"rowserrcheck"},{"Name":"staticcheck","Enabled":true,"EnabledByDefault":true},{"Name":"unused","Enabled":true,"EnabledByDefault":true},{"Name":"gosimple","Enabled":true,"EnabledByDefault":true},{"Name":"stylecheck"},{"Name":"gosec"},{"Name":"structcheck","Enabled":true,"EnabledByDefault":true},{"Name":"varcheck","Enabled":true,"EnabledByDefault":true},{"Name":"interfacer"},{"Name":"unconvert"},{"Name":"ineffassign","Enabled":true,"EnabledByDefault":true},{"Name":"dupl"},{"Name":"goconst"},{"Name":"deadcode","Enabled":true,"EnabledByDefault":true},{"Name":"gocyclo"},{"Name":"cyclop"},{"Name":"gocognit"},{"Name":"typecheck","Enabled":true,"EnabledByDefault":true},{"Name":"asciicheck"},{"Name":"gofmt"},{"Name":"gofumpt"},{"Name":"goimports"},{"Name":"goheader"},{"Name":"gci"},{"Name":"maligned"},{"Name":"depguard"},{"Name":"misspell"},{"Name":"lll"},{"Name":"unparam"},{"Name":"dogsled"},{"Name":"nakedret"},{"Name":"prealloc"},{"Name":"scopelint"},{"Name":"gocritic"},{"Name":"gochecknoinits"},{"Name":"gochecknoglobals"},{"Name":"godox"},{"Name":"funlen"},{"Name":"whitespace"},{"Name":"wsl"},{"Name":"goprintffuncname"},{"Name":"gomnd"},{"Name":"goerr113"},{"Name":"gomodguard"},{"Name":"godot"},{"Name":"testpackage"},{"Name":"nestif"},{"Name":"exportloopref"},{"Name":"exhaustive"},{"Name":"sqlclosecheck"},{"Name":"nlreturn"},{"Name":"wrapcheck"},{"Name":"thelper"},{"Name":"tparallel"},{"Name":"exhaustivestruct"},{"Name":"errorlint"},{"Name":"paralleltest"},{"Name":"makezero"},{"Name":"forbidigo"},{"Name":"ifshort"},{"Name":"predeclared"},{"Name":"revive"},{"Name":"durationcheck"},{"Name":"wastedassign"},{"Name":"importas"},{"Name":"nilerr"},{"Name":"forcetypeassert"},{"Name":"gomoddirectives"},{"Name":"promlinter"},{"Name":"tagliatelle"},{"Name":"errname"},{"Name":"ireturn"},{"Name":"nilnil"},{"Name":"tenv"},{"Name":"contextcheck"},{"Name":"varnamelen"},{"Name":"bidichk"},{"Name":"nolintlint"}]}}
{"Issues":[{"FromLinter":"typecheck","Text":"undeclared name: `GetBankNameById`","Severity":"","SourceLines":["\tbankName, err := GetBankNameById(bankNameId)"],"Replacement":null,"Pos":{"Filename":"internal/operator/bank_branch_operator.go","Offset":0,"Line":67,"Column":19},"ExpectNoLint":false,"ExpectedNoLintLinter":""},{"FromLinter":"typecheck","Text":"undeclared name: `GetBankNameById`","Severity":"","SourceLines":["\tbankName, err := GetBankNameById(bankNameId)"],"Replacement":null,"Pos":{"Filename":"internal/operator/bank_branch_operator.go","Offset":0,"Line":98,"Column":19},"ExpectNoLint":false,"ExpectedNoLintLinter":""}],"Report":{"Linters":[{"Name":"govet","Enabled":true,"EnabledByDefault":true},{"Name":"bodyclose"},{"Name":"noctx"},{"Name":"errcheck","Enabled":true,"EnabledByDefault":true},{"Name":"golint"},{"Name":"rowserrcheck"},{"Name":"staticcheck","Enabled":true,"EnabledByDefault":true},{"Name":"unused","Enabled":true,"EnabledByDefault":true},{"Name":"gosimple","Enabled":true,"EnabledByDefault":true},{"Name":"stylecheck"},{"Name":"gosec"},{"Name":"structcheck","Enabled":true,"EnabledByDefault":true},{"Name":"varcheck","Enabled":true,"EnabledByDefault":true},{"Name":"interfacer"},{"Name":"unconvert"},{"Name":"ineffassign","Enabled":true,"EnabledByDefault":true},{"Name":"dupl"},{"Name":"goconst"},{"Name":"deadcode","Enabled":true,"EnabledByDefault":true},{"Name":"gocyclo"},{"Name":"cyclop"},{"Name":"gocognit"},{"Name":"typecheck","Enabled":true,"EnabledByDefault":true},{"Name":"asciicheck"},{"Name":"gofmt"},{"Name":"gofumpt"},{"Name":"goimports"},{"Name":"goheader"},{"Name":"gci"},{"Name":"maligned"},{"Name":"depguard"},{"Name":"misspell"},{"Name":"lll"},{"Name":"unparam"},{"Name":"dogsled"},{"Name":"nakedret"},{"Name":"prealloc"},{"Name":"scopelint"},{"Name":"gocritic"},{"Name":"gochecknoinits"},{"Name":"gochecknoglobals"},{"Name":"godox"},{"Name":"funlen"},{"Name":"whitespace"},{"Name":"wsl"},{"Name":"goprintffuncname"},{"Name":"gomnd"},{"Name":"goerr113"},{"Name":"gomodguard"},{"Name":"godot"},{"Name":"testpackage"},{"Name":"nestif"},{"Name":"exportloopref"},{"Name":"exhaustive"},{"Name":"sqlclosecheck"},{"Name":"nlreturn"},{"Name":"wrapcheck"},{"Name":"thelper"},{"Name":"tparallel"},{"Name":"exhaustivestruct"},{"Name":"errorlint"},{"Name":"paralleltest"},{"Name":"makezero"},{"Name":"forbidigo"},{"Name":"ifshort"},{"Name":"predeclared"},{"Name":"revive"},{"Name":"durationcheck"},{"Name":"wastedassign"},{"Name":"importas"},{"Name":"nilerr"},{"Name":"forcetypeassert"},{"Name":"gomoddirectives"},{"Name":"promlinter"},{"Name":"tagliatelle"},{"Name":"errname"},{"Name":"ireturn"},{"Name":"nilnil"},{"Name":"tenv"},{"Name":"contextcheck"},{"Name":"varnamelen"},{"Name":"bidichk"},{"Name":"nolintlint"}]}}
"""
    with open(path, mode='w') as f:
        f.write(data)


if __name__ == '__main__':

    # Lint env:
    # docker run --rm -it -v $(pwd):/app -w /app golangci/golangci-lint:v1.43.0 sh
    # golangci-lint run {gofile} --sort-results=true --tests=false --out-format html > lint_report.html
    # golangci-lint run {gofile} --sort-results=true --tests=false --out-format json >> lint_results.json
    #

    # image: python:3.7.2
    # use image python:3.7.2 which supports external cmd like "curl" instead python:3.7.2-slim.
    #

    root_dir = '/tmp/test'
    in_path = f'{root_dir}/lint_results.json'
    if not in_path:
        try:
            in_path = sys.argv[1]
        except IndexError:
            raise ValueError('input path is not defined')

    create_test_data(in_path)
    issues = read_lint_issues(in_path)
    if len(issues) == 0:
        exit(0)

    out_path = f'{root_dir}/lint_report.html'
    if not out_path:
        try:
            out_path = sys.argv[2]
        except IndexError:
            raise ValueError('output path is not defined')

    issues = format_issues(issues)
    # print(json.dumps(issues, indent=2))
    generate_lint_html_report(issues, out_path)
    print_lint_summary(issues)
