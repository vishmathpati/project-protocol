class ProjectProtocol < Formula
  desc "Session protocol plugin for Claude Code and Codex"
  homepage "https://github.com/vishmathpati/project-protocol"
  url "https://github.com/vishmathpati/project-protocol/releases/download/v3.3.1/project-protocol-v3.3.1.plugin"
  sha256 "b61710d94845d345f0447c4331a1fdd54019d1133ebae4760c477347f658d3f1"
  version "3.3.1"
  license "MIT"

  def install
    # Store the plugin in the Homebrew cellar
    libexec.install "project-protocol-v#{version}.plugin" => "project-protocol.plugin"

    # Write a helper script so `project-protocol` activates the plugin
    (bin/"project-protocol").write <<~EOS
      #!/bin/bash
      set -e
      PLUGIN="#{libexec}/project-protocol.plugin"

      if command -v claude &> /dev/null; then
        claude plugin install "$PLUGIN"
        echo "✅ project-protocol v#{version} installed for Claude Code"
        echo ""
        echo "Open any project in Claude Code and say: init project"
      else
        echo "⚠️  Claude Code not found in PATH."
        echo "Install it from https://claude.ai/code, then run: project-protocol"
        echo ""
        echo "Or install manually: claude plugin install $PLUGIN"
        exit 1
      fi
    EOS
    chmod 0755, bin/"project-protocol"
  end

  def caveats
    <<~EOS
      Plugin is ready. Run this once to activate it in Claude Code:

        project-protocol

      Then open any project and say "init project" to set up the protocol.
    EOS
  end

  test do
    assert_predicate libexec/"project-protocol.plugin", :exist?
  end
end
