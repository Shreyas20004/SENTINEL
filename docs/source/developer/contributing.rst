.. _developer-contributing:

=======================
Contributing Guide
=======================

How to contribute to SENTINEL.

Code of Conduct
===============

We are committed to providing a welcoming and inspiring community for all.

- **Be respectful:** Treat all community members with respect
- **Be inclusive:** Welcome newcomers and diverse perspectives
- **Be constructive:** Provide and accept constructive feedback
- **Report issues:** Use private channels for security concerns

Violation reporting: `security@sentinel.dev`

Getting Started
===============

**Prerequisites:**

- GitHub account
- Git installed locally
- Python 3.11 + Node.js 20
- Docker & Docker Compose
- Read :ref:`developer-setup` and :ref:`developer-backend`

**1. Fork the repository**

.. code-block:: bash

   # On GitHub, click "Fork"
   git clone https://github.com/YOUR_USERNAME/sentinel.git
   cd sentinel

**2. Create development branch**

.. code-block:: bash

   git checkout -b feature/my-feature
   # or
   git checkout -b bugfix/issue-123

**Branch naming:**

- Features: `feature/short-description`
- Bugfixes: `bugfix/short-description`
- Documentation: `docs/short-description`
- Examples: `feature/yolov8-integration`, `bugfix/redis-timeout-fix`

**3. Set up development environment**

.. code-block:: bash

   # Backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   npm run dev

**4. Make changes**

Follow the coding standards below.

**5. Test locally**

.. code-block:: bash

   # Backend tests
   pytest tests/ -v
   
   # Frontend tests
   npm run test
   
   # Code quality
   black . && flake8 . && mypy .
   npm run lint

**6. Commit & push**

.. code-block:: bash

   git add .
   git commit -m "feat: add YOLOv8 inference"
   git push origin feature/my-feature

**7. Create pull request**

- Go to GitHub repository
- Click "New Pull Request"
- Select your branch
- Fill in PR title and description (see below)
- Click "Create Pull Request"

Pull Request Process
====================

**Title format:**

Short, descriptive, imperative mood:

- ✅ `feat: add YOLOv8 inference pipeline`
- ✅ `fix: resolve WebSocket reconnection timeout`
- ✅ `docs: update architecture guide`
- ❌ `Added YOLOv8` (not imperative)
- ❌ `Fix bug` (too vague)

**Description template:**

.. code-block:: markdown

   ## Description
   Brief explanation of changes
   
   ## Problem
   What issue does this solve?
   
   ## Solution
   How does this PR address the issue?
   
   ## Testing
   - [ ] Manual testing completed
   - [ ] Unit tests added
   - [ ] Integration tests passed
   - [ ] No breaking changes
   
   ## Checklist
   - [ ] Code follows style guide
   - [ ] Comments added for complex sections
   - [ ] Documentation updated
   - [ ] No new warnings/errors

**Review process:**

1. Automated checks run (tests, linting)
2. Maintainers review code
3. Feedback provided (if needed)
4. Changes requested are made
5. PR approved and merged
6. Branch deleted

**Merging:**

- Use "Squash and merge" for feature branches
- Use "Create a merge commit" for release branches
- Delete branch after merge

Coding Standards
================

**Python Backend:**

**Style guide:** PEP 8 + Black formatter

.. code-block:: python

   # Format code
   black backend/

   # Check style
   flake8 backend/

   # Type check
   mypy backend/

**Example (good code):**

.. code-block:: python

   """Incident detection service."""
   from typing import Optional
   from pydantic import BaseModel
   from sqlalchemy import select
   
   class IncidentCreate(BaseModel):
       """Request model for creating incidents."""
       zone_id: str
       severity: str
       description: str
   
   async def create_incident(
       db: AsyncSession,
       payload: IncidentCreate
   ) -> Incident:
       """Create new incident in database.
       
       Args:
           db: Database session
           payload: Incident creation data
       
       Returns:
           Created incident object
       """
       incident = Incident(**payload.model_dump())
       db.add(incident)
       await db.commit()
       await db.refresh(incident)
       return incident

**Key rules:**

- Max line length: 88 characters
- Docstrings for all functions/classes
- Type hints on all parameters
- Async/await for all I/O operations
- No bare `except:`
- No `print()` — use logging

**TypeScript Frontend:**

**Style guide:** ESLint + Prettier

.. code-block:: bash

   npm run lint -- --fix
   npm run format

**Example (good code):**

.. code-block:: typescript

   /**
    * Display list of incidents in severity order.
    * Listens for real-time updates via WebSocket.
    */
   export const ThreatQueue: React.FC<ThreatQueueProps> = ({
     onEscalate
   }) => {
     const [incidents, setIncidents] = useState<Incident[]>([]);
     const [loading, setLoading] = useState(false);
     
     useEffect(() => {
       // Fetch initial incidents
       const fetchIncidents = async () => {
         setLoading(true);
         const data = await apiClient.getIncidents();
         setIncidents(data);
         setLoading(false);
       };
       
       fetchIncidents();
       
       // Listen for real-time updates
       wsService.on('alert', (alert: Alert) => {
         setIncidents(prev => [alert, ...prev]);
       });
       
       return () => wsService.off('alert');
     }, []);
     
     if (loading) return <div>Loading...</div>;
     
     return (
       <div>
         {incidents.map(incident => (
           <IncidentItem
             key={incident.id}
             incident={incident}
             onEscalate={() => onEscalate(incident.id)}
           />
         ))}
       </div>
     );
   };

**Key rules:**

- Max line length: 100 characters
- JSDoc for exported functions
- Type all Props interfaces
- const > let > var
- No `any` types (use `unknown` with type guards)
- Memoize expensive components

Testing Standards
=================

**Backend testing (pytest):**

.. code-block:: python

   # tests/test_incidents.py
   import pytest
   from app.api.incidents import create_incident
   from app.schemas import IncidentCreate
   
   @pytest.mark.asyncio
   async def test_create_incident_high_severity(db_session):
       """Test creating HIGH severity incident."""
       payload = IncidentCreate(
           zone_id="zone_1",
           severity="HIGH",
           description="Test incident"
       )
       
       incident = await create_incident(db_session, payload)
       
       assert incident.id is not None
       assert incident.severity == "HIGH"
       assert incident.status == "OPEN"

**Frontend testing (React Testing Library):**

.. code-block:: typescript

   import { render, screen, waitFor } from '@testing-library/react';
   import { ThreatQueue } from './ThreatQueue';
   
   test('displays incidents in severity order', async () => {
       vi.mocked(apiClient.getIncidents).mockResolvedValue([
           { id: '1', severity: 'MED' },
           { id: '2', severity: 'HIGH' }
       ]);
       
       render(<ThreatQueue />);
       
       await waitFor(() => {
           const items = screen.getAllByRole('listitem');
           expect(items[0]).toHaveTextContent('HIGH');
       });
   });

**Coverage requirements:**

- New code: ≥80% unit test coverage
- Critical paths: ≥95% coverage
- Run: `pytest --cov=backend/app tests/`

Documentation Standards
=======================

**In-code comments:**

.. code-block:: python

   # Good: Explains WHY, not WHAT
   # Use ByteTrack instead of simple distance-based matching
   # because centroid shifts significantly with bbox jitter
   for detection in detections:
       track_id = match_with_existing_tracks(detection)
   
   # Avoid: Obvious comment
   # i = 0  # Set i to zero

**Docstrings (PEP 257):**

.. code-block:: python

   def calculate_risk_score(
       incident: Incident,
       historical_data: dict
   ) -> float:
       """Calculate threat risk score (0-100).
       
       Args:
           incident: Incident to analyze
           historical_data: Historical incident patterns
       
       Returns:
           Risk score from 0 (safe) to 100 (critical)
       
       Raises:
           ValueError: If incident severity invalid
       
       Example:
           >>> score = calculate_risk_score(incident, {})
           >>> 0 <= score <= 100
           True
       """

**Documentation updates:**

- Update README.md for user-facing changes
- Update relevant .rst files in docs/source/
- Update inline code comments for non-obvious logic
- Update CHANGELOG.md with summary

Git Workflow Best Practices
===========================

**Commit messages (Conventional Commits):**

.. code-block:: text

   feat: add YOLOv8 inference
   
   Implement YOLOv8 model loading and frame inference
   with <50ms latency target on GPU.
   
   Closes #234

**Common types:**

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `refactor:` code refactoring (no behavior change)
- `perf:` performance improvements
- `test:` test additions/updates
- `chore:` build, dependencies, etc.

**Keep commits small & focused:**

.. code-block:: bash

   # ✅ Good: Related changes in one commit
   git commit -m "feat: add YOLOv8 inference and unit tests"
   
   # ❌ Avoid: Mixing unrelated changes
   git commit -m "feat: add YOLOv8, fix webhook timeout, update docs"

**Push regularly:**

.. code-block:: bash

   # Push at least daily
   git push origin feature/my-feature

Common Pit Falls
================

❌ **Not writing tests**
   → Tests are mandatory for new features

❌ **Breaking changes without documentation**
   → Document in CHANGELOG.md with migration steps

❌ **Ignoring lint errors**
   → Run `black`, `flake8`, `mypy` before push

❌ **Committing secrets**
   → Store in .env (gitignored) or use secrets management

❌ **Very long-lived branches**
   → Merge within 1-2 weeks of opening PR

❌ **Vague PR descriptions**
   → Be specific about what and why

Performance Checklist
=====================

Before submitting PR, verify:

- [ ] Database queries use proper indexes
- [ ] No N+1 query problems
- [ ] API responses < 100ms
- [ ] Frontend components memoized if needed
- [ ] No unintended polling or subscriptions
- [ ] Unused imports removed
- [ ] No memory leaks in WebSocket handlers

Release Process
===============

**Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)

Example: v1.2.3

- MAJOR: Breaking changes (1.0.0 → 2.0.0)
- MINOR: New features (1.0.0 → 1.1.0)
- PATCH: Bug fixes (1.0.0 → 1.0.1)

**Release workflow:**

.. code-block:: bash

   # Create release branch
   git checkout -b release/v1.2.0
   
   # Update version numbers
   # - package.json
   # - backend/app/__init__.py
   # - docs/conf.py
   
   # Update CHANGELOG.md
   # Commit changes
   git add .
   git commit -m "chore: release v1.2.0"
   
   # Tag release
   git tag v1.2.0
   
   # Push & merge to main
   git push origin release/v1.2.0
   git push origin v1.2.0

Getting Help
============

**Questions?**

- Check documentation at readthedocs.io
- Search existing GitHub issues
- Ask in GitHub discussions
- Email team: `dev@sentinel.dev`

**Found a bug?**

- Create GitHub issue with:

  * Reproducible steps
  * Expected vs actual behavior
  * Environment (OS, Python ver, etc.)
  * Error logs

**Security issue?**

- Report to: `security@sentinel.dev`
- Do NOT open public issue
- Include vulnerability details and impact

Recognition
===========

Contributors with 5+ merged PRs get:

- ✨ Listed in CONTRIBUTORS.md
- 🏆 Contributor role on Discord
- 📚 Knowledge base article featuring work
- 💼 Resume reference from project

Community
=========

**Get involved:**

- ⭐ Star the repo
- 💬 Join Discord (see README.md)
- 📢 Share ideas on GitHub discussions
- 🐛 Help triage issues
- 📝 Write blog posts about SENTINEL
- 🎓 Create tutorials for YouTube

**Community events:**

- Monthly community calls (1st Thursday)
- Quarterly hackathons
- Annual conference (Phase 4+)

Thank You!
==========

We appreciate every contribution, no matter how small.

Together, we're building the future of public safety.

--------

**Last Updated:** March 29, 2026

**Questions?** Open an issue on GitHub!
