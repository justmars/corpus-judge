import pytest

from corpus_judge import CandidateJustice, JusticeDetail


@pytest.fixture
def candidate_list(session):
    return CandidateJustice(
        db=session,
        date_str="Dec. 1, 1995",
    )


def test_justice_candidate(candidate_list):
    assert len(candidate_list.rows) == 15


@pytest.fixture
def candidate(session):
    return CandidateJustice(
        db=session,
        text="Panganiban, Acting Cj",
        date_str="Dec. 1, 1995",
    )


@pytest.fixture
def candidate_as_cj(session):
    return CandidateJustice(db=session, text="Panganiban", date_str="2006-03-30")


def test_justice_choice(candidate):
    assert candidate.choice == {
        "id": 137,
        "full_name": "Artemio V. Panganiban",
        "surname": "Panganiban",
        "start_term": "1995-10-05",
        "inactive_date": "2006-12-06",
        "chief_date": "2005-12-20",
        "designation": "J.",
    }


def test_justice_ponencia(candidate):
    assert candidate.ponencia == {
        "justice_id": candidate.id,
        "raw_ponente": candidate.raw_ponente,
        "per_curiam": candidate.per_curiam,
    }


def test_justice_detail_generic_designation(candidate):
    assert candidate.detail == JusticeDetail(
        justice_id=137,
        raw_ponente="Panganiban",
        designation="J.",
        per_curiam=False,
    )


def test_justice_detail_cj_designation(candidate_as_cj):
    assert candidate_as_cj.detail == JusticeDetail(
        justice_id=137,
        raw_ponente="Panganiban",
        designation="C.J.",
        per_curiam=False,
    )
