from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models import mint_snapshot, get_snapshot, get_snapshots_by_owner

routes = Blueprint("routes", __name__)


@routes.route('/')
def home():
    return render_template("index.html")


@routes.route('/upload')
def upload_page():
    return render_template("upload.html")


@routes.route('/verify')
def verify_page():
    return render_template("verify.html")


@routes.route('/submission_success')
def submission_success():
    tx_hash = request.args.get("tx_hash")
    token_id = request.args.get("token_id")
    return render_template("submission_success.html", tx_hash=tx_hash, token_id=token_id)


@routes.route('/upload_credit_report', methods=['POST'])
def upload_credit_report():
    """Mint a credit snapshot NFT."""
    data = request.json
    wallet_address = data.get("wallet_address")
    credit_score = data.get("credit_score")

    if not wallet_address or not credit_score:
        return jsonify({"error": "Missing wallet_address or credit_score"}), 400

    try:
        credit_score = int(credit_score)
    except ValueError:
        return jsonify({"error": "credit_score must be a number"}), 400

    if credit_score < 300 or credit_score > 850:
        return jsonify({"error": "Credit score must be between 300 and 850"}), 400

    result = mint_snapshot(wallet_address, credit_score)

    return jsonify({
        "message": "Credit snapshot NFT minted",
        "redirect_url": url_for('routes.submission_success',
                                tx_hash=result["tx_hash"],
                                token_id=result["token_id"])
    })


@routes.route('/get_credit_report', methods=['POST'])
def get_credit_report():
    """Retrieve snapshots by wallet address or token ID."""
    data = request.json
    wallet_address = data.get("wallet_address")
    token_id = data.get("token_id")

    if token_id is not None:
        try:
            snapshot = get_snapshot(token_id)
            return jsonify(snapshot)
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    if wallet_address:
        try:
            snapshots = get_snapshots_by_owner(wallet_address)
            return jsonify({"snapshots": snapshots, "wallet_address": wallet_address})
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    return jsonify({"error": "Provide wallet_address or token_id"}), 400
