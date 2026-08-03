import { CampaignStatus } from "@/types/campaign";


interface Props {
    status: CampaignStatus;
}


export default function StatusBadge({
    status
}: Props) {

    return (
        <span className="px-2 py-1 rounded text-sm bg-gray-100">
            {status}
        </span>
    );
}