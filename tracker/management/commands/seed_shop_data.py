from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tracker.models import (
    Batch,
    Distributor,
    Manufacturer,
    Pharmacy,
    PharmacyInventory,
    Transaction,
)


class Command(BaseCommand):
    help = "Seed blockchain-linked sample batches and pharmacy inventory for patient shop."

    def handle(self, *args, **options):
        manufacturer, _ = Manufacturer.objects.get_or_create(
            wallet_address="addr_test1qmanufacturerseed",
            defaults={"name": "PharmaCorp Ltd.", "verified": True},
        )
        if not manufacturer.verified:
            manufacturer.verified = True
            manufacturer.save(update_fields=["verified"])

        distributor, _ = Distributor.objects.get_or_create(
            wallet_address="addr_test1qdistributorseed",
            defaults={"name": "MediDistribute Inc.", "verified": True},
        )
        if not distributor.verified:
            distributor.verified = True
            distributor.save(update_fields=["verified"])

        pharmacy, _ = Pharmacy.objects.get_or_create(
            wallet_address="addr_test1qpharmacyseed",
            defaults={"name": "CityCare Pharmacy", "verified": True},
        )
        if not pharmacy.verified:
            pharmacy.verified = True
            pharmacy.save(update_fields=["verified"])

        sample_batches = [
            {
                "batch_id": "BATCH-2026-001",
                "medicine_name": "Paracetamol 500mg",
                "composition": "Paracetamol 500mg",
                "manufactured_date": "2026-01-10",
                "expiry_date": "2028-01-10",
                "quantity": 12000,
                "price": Decimal("6500.00"),
                "stock": 350,
            },
            {
                "batch_id": "BATCH-2026-002",
                "medicine_name": "Cefuroxime 500mg",
                "composition": "Cefuroxime 500mg",
                "manufactured_date": "2026-01-25",
                "expiry_date": "2028-01-25",
                "quantity": 6000,
                "price": Decimal("5000.00"),
                "stock": 160,
            },
            {
                "batch_id": "BATCH-2026-003",
                "medicine_name": "Amoxicillin 250mg",
                "composition": "Amoxicillin 250mg",
                "manufactured_date": "2026-02-08",
                "expiry_date": "2028-02-08",
                "quantity": 9000,
                "price": Decimal("4000.00"),
                "stock": 240,
            },
            {
                "batch_id": "BATCH-2026-004",
                "medicine_name": "Cough Syrup 100ml",
                "composition": "Dextromethorphan + Guaifenesin",
                "manufactured_date": "2026-02-20",
                "expiry_date": "2027-08-20",
                "quantity": 5000,
                "price": Decimal("5000.00"),
                "stock": 180,
            },
            {
                "batch_id": "BATCH-2026-005",
                "medicine_name": "Artemether Injection 80mg/1ml",
                "composition": "Artemether 80mg/1ml",
                "manufactured_date": "2026-03-02",
                "expiry_date": "2027-09-02",
                "quantity": 3000,
                "price": Decimal("8000.00"),
                "stock": 120,
            },
            {
                "batch_id": "BATCH-2026-006",
                "medicine_name": "Ibuprofen 400mg",
                "composition": "Ibuprofen 400mg",
                "manufactured_date": "2026-03-12",
                "expiry_date": "2028-03-12",
                "quantity": 7000,
                "price": Decimal("3500.00"),
                "stock": 260,
            },
            {
                "batch_id": "BATCH-2026-007",
                "medicine_name": "Azithromycin 500mg",
                "composition": "Azithromycin 500mg",
                "manufactured_date": "2026-03-20",
                "expiry_date": "2028-03-20",
                "quantity": 5000,
                "price": Decimal("9000.00"),
                "stock": 140,
            },
            {
                "batch_id": "BATCH-2026-008",
                "medicine_name": "Metronidazole 400mg",
                "composition": "Metronidazole 400mg",
                "manufactured_date": "2026-04-01",
                "expiry_date": "2028-04-01",
                "quantity": 8000,
                "price": Decimal("3200.00"),
                "stock": 300,
            },
            {
                "batch_id": "BATCH-2026-009",
                "medicine_name": "Vitamin C 1000mg",
                "composition": "Ascorbic Acid 1000mg",
                "manufactured_date": "2026-04-10",
                "expiry_date": "2028-04-10",
                "quantity": 7500,
                "price": Decimal("2800.00"),
                "stock": 220,
            },
            {
                "batch_id": "BATCH-2026-010",
                "medicine_name": "Omeprazole 20mg",
                "composition": "Omeprazole 20mg",
                "manufactured_date": "2026-04-18",
                "expiry_date": "2028-04-18",
                "quantity": 6500,
                "price": Decimal("4200.00"),
                "stock": 170,
            },
            {
                "batch_id": "BATCH-2026-011",
                "medicine_name": "Cetirizine 10mg",
                "composition": "Cetirizine 10mg",
                "manufactured_date": "2026-04-25",
                "expiry_date": "2028-04-25",
                "quantity": 9000,
                "price": Decimal("2500.00"),
                "stock": 260,
            },
            {
                "batch_id": "BATCH-2026-012",
                "medicine_name": "ORS Sachet",
                "composition": "Oral Rehydration Salts",
                "manufactured_date": "2026-05-02",
                "expiry_date": "2028-05-02",
                "quantity": 12000,
                "price": Decimal("1200.00"),
                "stock": 400,
            },

            {
                "batch_id": "BATCH-2026-014",
                "medicine_name": "Losartan 50mg",
                "composition": "Losartan Potassium 50mg",
                "manufactured_date": "2026-05-15",
                "expiry_date": "2028-05-15",
                "quantity": 5500,
                "price": Decimal("4800.00"),
                "stock": 180,
            },
            {
                "batch_id": "BATCH-2026-015",
                "medicine_name": "Metformin 500mg",
                "composition": "Metformin 500mg",
                "manufactured_date": "2026-05-20",
                "expiry_date": "2028-05-20",
                "quantity": 9000,
                "price": Decimal("3000.00"),
                "stock": 260,
            },
            {
                "batch_id": "BATCH-2026-016",
                "medicine_name": "Atorvastatin 20mg",
                "composition": "Atorvastatin 20mg",
                "manufactured_date": "2026-05-28",
                "expiry_date": "2028-05-28",
                "quantity": 4200,
                "price": Decimal("6200.00"),
                "stock": 140,
            },
            {
                "batch_id": "BATCH-2026-017",
                "medicine_name": "Ciprofloxacin 500mg",
                "composition": "Ciprofloxacin 500mg",
                "manufactured_date": "2026-06-03",
                "expiry_date": "2028-06-03",
                "quantity": 4800,
                "price": Decimal("5500.00"),
                "stock": 160,
            },
            {
                "batch_id": "BATCH-2026-018",
                "medicine_name": "Doxycycline 100mg",
                "composition": "Doxycycline 100mg",
                "manufactured_date": "2026-06-08",
                "expiry_date": "2028-06-08",
                "quantity": 5000,
                "price": Decimal("4200.00"),
                "stock": 190,
            },
            {
                "batch_id": "BATCH-2026-019",
                "medicine_name": "Co-trimoxazole 960mg",
                "composition": "Sulfamethoxazole 800mg + Trimethoprim 160mg",
                "manufactured_date": "2026-06-12",
                "expiry_date": "2028-06-12",
                "quantity": 7000,
                "price": Decimal("3600.00"),
                "stock": 240,
            },
            {
                "batch_id": "BATCH-2026-020",
                "medicine_name": "Hydrocortisone Cream 1%",
                "composition": "Hydrocortisone 1%",
                "manufactured_date": "2026-06-18",
                "expiry_date": "2027-12-18",
                "quantity": 3500,
                "price": Decimal("3000.00"),
                "stock": 130,
            },
            {
                "batch_id": "BATCH-2026-021",
                "medicine_name": "Folic Acid 5mg",
                "composition": "Folic Acid 5mg",
                "manufactured_date": "2026-06-22",
                "expiry_date": "2028-06-22",
                "quantity": 10000,
                "price": Decimal("1500.00"),
                "stock": 320,
            },
            {
                "batch_id": "BATCH-2026-022",
                "medicine_name": "Zinc Sulfate 20mg",
                "composition": "Zinc Sulfate 20mg",
                "manufactured_date": "2026-06-28",
                "expiry_date": "2028-06-28",
                "quantity": 9000,
                "price": Decimal("1400.00"),
                "stock": 300,
            },
            {
                "batch_id": "BATCH-2026-023",
                "medicine_name": "Salbutamol Inhaler 100mcg",
                "composition": "Salbutamol 100mcg",
                "manufactured_date": "2026-07-02",
                "expiry_date": "2028-07-02",
                "quantity": 2500,
                "price": Decimal("8500.00"),
                "stock": 110,
            },
            {
                "batch_id": "BATCH-2026-024",
                "medicine_name": "Ranitidine 150mg",
                "composition": "Ranitidine 150mg",
                "manufactured_date": "2026-07-08",
                "expiry_date": "2028-07-08",
                "quantity": 5200,
                "price": Decimal("2600.00"),
                "stock": 180,
            },
            {
                "batch_id": "BATCH-2026-025",
                "medicine_name": "Loratadine 10mg",
                "composition": "Loratadine 10mg",
                "manufactured_date": "2026-07-12",
                "expiry_date": "2028-07-12",
                "quantity": 7800,
                "price": Decimal("2300.00"),
                "stock": 240,
            },
            {
                "batch_id": "BATCH-2026-026",
                "medicine_name": "Diclofenac 50mg",
                "composition": "Diclofenac 50mg",
                "manufactured_date": "2026-07-18",
                "expiry_date": "2028-07-18",
                "quantity": 6200,
                "price": Decimal("3100.00"),
                "stock": 200,
            },
            {
                "batch_id": "BATCH-2026-027",
                "medicine_name": "Prednisolone 5mg",
                "composition": "Prednisolone 5mg",
                "manufactured_date": "2026-07-22",
                "expiry_date": "2028-07-22",
                "quantity": 4500,
                "price": Decimal("2700.00"),
                "stock": 150,
            },
        ]

        seeded = 0
        for item in sample_batches:
            batch, created = Batch.objects.get_or_create(
                batch_id=item["batch_id"],
                defaults={
                    "medicine_name": item["medicine_name"],
                    "composition": item["composition"],
                    "manufacturer": manufacturer,
                    "manufactured_date": item["manufactured_date"],
                    "expiry_date": item["expiry_date"],
                    "quantity": item["quantity"],
                    "policy_id": "seed_policy_testnet",
                    "asset_name": item["batch_id"].replace("-", "").lower(),
                    "nft_minted": True,
                    "qr_code": f"qr-{item['batch_id'].lower()}",
                },
            )

            if not created:
                batch.medicine_name = item["medicine_name"]
                batch.composition = item["composition"]
                batch.manufacturer = manufacturer
                batch.manufactured_date = item["manufactured_date"]
                batch.expiry_date = item["expiry_date"]
                batch.quantity = item["quantity"]
                batch.policy_id = "seed_policy_testnet"
                batch.asset_name = item["batch_id"].replace("-", "").lower()
                batch.nft_minted = True
                if not batch.qr_code:
                    batch.qr_code = f"qr-{item['batch_id'].lower()}"
                batch.save()

            Transaction.objects.get_or_create(
                tx_hash=f"seed-mint-{item['batch_id'].lower()}",
                defaults={
                    "batch": batch,
                    "transaction_type": "MINT",
                    "to_wallet": manufacturer.wallet_address,
                },
            )
            Transaction.objects.get_or_create(
                tx_hash=f"seed-transfer-md-{item['batch_id'].lower()}",
                defaults={
                    "batch": batch,
                    "transaction_type": "TRANSFER",
                    "from_wallet": manufacturer.wallet_address,
                    "to_wallet": distributor.wallet_address,
                },
            )
            Transaction.objects.get_or_create(
                tx_hash=f"seed-transfer-dp-{item['batch_id'].lower()}",
                defaults={
                    "batch": batch,
                    "transaction_type": "TRANSFER",
                    "from_wallet": distributor.wallet_address,
                    "to_wallet": pharmacy.wallet_address,
                },
            )

            PharmacyInventory.objects.update_or_create(
                pharmacy=pharmacy,
                batch=batch,
                defaults={
                    "quantity_available": item["stock"],
                    "price_per_unit": item["price"],
                    "in_stock": item["stock"] > 0,
                },
            )
            seeded += 1

        # Optional quick demo patient account
        if not User.objects.filter(username="patientdemo").exists():
            User.objects.create_user(
                username="patientdemo",
                password="patientdemo123",
                email="patientdemo@example.com",
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {seeded} blockchain-linked batches and inventory items ready."
            )
        )
