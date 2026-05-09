cask "project-protocol" do
  version "3.3.1"
  sha256 "b61710d94845d345f0447c4331a1fdd54019d1133ebae4760c477347f658d3f1"

  url "https://github.com/vishmathpati/project-protocol/releases/download/v#{version}/project-protocol-v#{version}.plugin"
  name "project-protocol"
  desc "Session protocol plugin for Claude Code and Codex"
  homepage "https://github.com/vishmathpati/project-protocol"

  # Copy plugin to a permanent location so it survives staging cleanup
  artifact "project-protocol-v#{version}.plugin",
    target: "#{Dir.home}/Library/Application Support/project-protocol/project-protocol.plugin"

  postflight do
    plugin_path = "#{Dir.home}/Library/Application Support/project-protocol/project-protocol.plugin"

    # Search common Claude Code install locations — brew PATH is restricted
    claude = %w[
      claude
      /usr/local/bin/claude
      /opt/homebrew/bin/claude
    ].find { |p| system("/usr/bin/env", "test", "-x", p) || system("command", "-v", p) }

    if claude
      system_command "/bin/bash",
        args: ["-c", "#{claude} plugin install '#{plugin_path}' && echo '✅ project-protocol installed.'"],
        print_stdout: true
    else
      puts ""
      puts "⚠️  Claude Code not found in PATH during install."
      puts "Run this once to activate the plugin:"
      puts "  claude plugin install '#{plugin_path}'"
      puts ""
    end
  end

  zap trash: ["#{Dir.home}/Library/Application Support/project-protocol"]
end
