cask "project-protocol" do
  version "3.3.1"
  sha256 "b61710d94845d345f0447c4331a1fdd54019d1133ebae4760c477347f658d3f1"

  url "https://github.com/vishmathpati/project-protocol/releases/download/v#{version}/project-protocol-v#{version}.plugin"
  name "project-protocol"
  desc "Session protocol plugin for Claude Code and Codex"
  homepage "https://github.com/vishmathpati/project-protocol"

  # No .app bundle — install via claude plugin install
  postflight do
    system_command "/bin/bash",
      args: [
        "-c",
        "if command -v claude &>/dev/null; then " \
          "claude plugin install '#{staged_path}/project-protocol-v#{version}.plugin' && " \
          "echo '✅ project-protocol installed. Open any project and say: init project'; " \
        "else " \
          "echo '⚠️  Claude Code not found. Install from https://claude.ai/code then run:'; " \
          "echo '    brew reinstall --cask vishmathpati/project-protocol/project-protocol'; " \
        "fi"
      ],
      print_stdout: true
  end

  zap trash: []
end
