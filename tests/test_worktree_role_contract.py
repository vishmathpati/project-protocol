from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


class WorktreeRoleContractTests(unittest.TestCase):
    def test_roles_are_independent_of_checkout_topology(self):
        solo = read("skills/solo/SKILL.md")
        ceo = read("skills/ceo/SKILL.md")
        git = read("skills/git/SKILL.md")

        self.assertNotIn("with no worktree", solo)
        self.assertNotIn("No worktree", solo)
        self.assertIn("either is valid", solo)
        self.assertIn("role authority is independent of checkout topology", ceo)
        self.assertIn("checkout topology never selects the role", git)
        self.assertIn("If an app-created worktree starts at detached HEAD", git)

    def test_local_checkout_is_supported_with_one_time_recommendation(self):
        recap = read("skills/recap/SKILL.md")
        worker = read("skills/worker/SKILL.md")
        git = read("skills/git/SKILL.md")

        for content in (recap, git):
            self.assertIn("A worktree is recommended", content)
            self.assertIn("one-time", content.lower())
        self.assertIn("Local checkout is supported", worker)
        self.assertIn("dedicated `ch-NN-name` branch", worker)

    def test_handoff_can_resume_in_fresh_worktree_without_losing_dirty_state(self):
        handoff = read("skills/handoff/SKILL.md")

        self.assertIn("fresh app-created worktree", handoff)
        self.assertIn("recorded working branch or checkpoint commit", handoff)
        self.assertIn("cannot recover another checkout's dirty files", handoff)

    def test_save_session_handles_ceo_and_solo_worktrees(self):
        save = read("skills/save-session/SKILL.md")

        self.assertIn("In a CEO worktree", save)
        self.assertIn("current local checkout or worktree", save)

    def test_recap_does_not_call_main_checkout_the_real_files(self):
        recap = read("skills/recap/SKILL.md")

        self.assertIn("isolated real checkout", recap)
        self.assertNotIn("so the user knows where the real files live", recap)
        self.assertIn("never call one checkout", recap)


if __name__ == "__main__":
    unittest.main()
