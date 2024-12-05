from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Election, Candidate, Vote
from .encryption.homomorphic import HomomorphicEncryption
from .encryption.FernetEncryptor import FernetEncryptor

homomorphic_encryptor = HomomorphicEncryption()
fernet_encryptor = FernetEncryptor()

def home(request):
    election = get_active_election()
    candidates = Candidate.objects.filter(election=election)
    return render(request, 'voting_app/home.html', {'candidates': candidates})


@login_required
def vote(request):
    election = get_active_election()
    candidates = Candidate.objects.filter(election=election)
    existing_vote = Vote.objects.filter(voter=request.user.username, election=election).first()

    if existing_vote:
        messages.error(request, "You have already voted in this election.")
        return redirect(reverse("voting_app:home"))

    if request.method == 'POST':
        selected_candidate_id = request.POST.get("candidate")
        selected_candidate = Candidate.objects.get(id=selected_candidate_id)

        # Encrypt and store the vote
        encrypted_vote = homomorphic_encryptor.encrypt(1)

        cipher_text = str(encrypted_vote.ciphertext())
        exponent = str(encrypted_vote.exponent)

        encrypted_cipher_text = fernet_encryptor.encrypt(cipher_text).decode()
        encrypted_exponent = fernet_encryptor.encrypt(exponent).decode()

        Vote.objects.create(
            voter=request.user.username, 
            election=election,
            candidate=selected_candidate,
            cipher_text=encrypted_cipher_text,
            exponent=encrypted_exponent)
        
        # Encrypt and store the vote for the rest of candidates
        for candidate in candidates:
            if candidate == selected_candidate: continue
            encrypted_vote = homomorphic_encryptor.encrypt(0)

            cipher_text = str(encrypted_vote.ciphertext())
            exponent = str(encrypted_vote.exponent)

            encrypted_cipher_text = fernet_encryptor.encrypt(cipher_text).decode()
            encrypted_exponent = fernet_encryptor.encrypt(exponent).decode()

            Vote.objects.create(
                voter=request.user.username, 
                election=election,
                candidate=selected_candidate,
                cipher_text=encrypted_cipher_text,
                exponent=encrypted_exponent)

        messages.success(request, "Your vote has been cast successfully!")
        
    return redirect(reverse("voting_app:home"))



def count_votes(request):
    election = get_active_election()
    candidates = {candidate:0 for candidate in Candidate.objects.filter(election=election)}
    all_votes = Vote.objects.filter(election=election)

    for candidate in candidates:
        candidate_votes = all_votes.filter(candidate=candidate)
        encrypted_votes = []
        for vote in candidate_votes:
            decrypted_cipher_text = fernet_encryptor.decrypt(vote.cipher_text).decode()
            decrypted_exponent = fernet_encryptor.decrypt(vote.exponent).decode()
            cipher = int(decrypted_cipher_text)
            exponent = int(decrypted_exponent)
            encrypted_votes.append(homomorphic_encryptor.generate_EncryptedNumber(cipher,exponent))

        total = homomorphic_encryptor.sum(encrypted_votes)
        candidates[candidate] = total

    results = [{"name":candidate.name, "total":candidates[candidate]} for candidate in candidates]
    return render(request, "voting_app/results.html",{'candidates': results})

def get_active_election():
    now = timezone.now()
    return Election.objects.filter(Q(start_date__lte=now) & Q(end_date__gte=now)).first()