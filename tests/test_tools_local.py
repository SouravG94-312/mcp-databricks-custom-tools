from tools.warranty_tools import get_warranty_claim_details_impl
from tools.service_tools import get_vehicle_service_history_impl
from tools.parts_tools import check_part_availability_impl
from tools.context_pack_tools import generate_aftermarket_context_pack_impl


def main():
    print("Testing warranty claim...")
    print(get_warranty_claim_details_impl("WC1001"))

    print("\nTesting service history...")
    print(get_vehicle_service_history_impl("VINDEF000123"))

    print("\nTesting part availability...")
    print(check_part_availability_impl("P001", "DE"))

    print("\nTesting context pack...")
    print(generate_aftermarket_context_pack_impl("dealer", "DLR003"))


if __name__ == "__main__":
    main()
